import hashlib
import hmac
import os
from pathlib import Path
import secrets
import sqlite3
import sys
from contextlib import contextmanager

from flask import Flask, jsonify, request

PROJECT_DIR = Path(__file__).resolve().parent.parent
if str(PROJECT_DIR) not in sys.path:
    sys.path.insert(0, str(PROJECT_DIR))

from auth_settings import AUTH_METHODS

LOCAL_METHODS = frozenset(AUTH_METHODS).intersection({'username', 'email'})
PASSWORD_ROUNDS = 310_000

@contextmanager
def connect_database(database_path):
    connection = sqlite3.connect(database_path)
    connection.row_factory = sqlite3.Row
    try:
        with connection:
            yield connection
    finally:
        connection.close()

def create_app(database_path=None):
    app = Flask(__name__)
    database_path = database_path or os.environ.get(
        'AUTH_DATABASE_PATH',
        str(PROJECT_DIR / 'users.sqlite3')
    )
    app.config['AUTH_DATABASE_PATH'] = database_path
    if database_path != ':memory:':
        Path(database_path).parent.mkdir(parents=True, exist_ok=True)

    with connect_database(database_path) as connection:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT COLLATE NOCASE UNIQUE,
                email TEXT COLLATE NOCASE UNIQUE,
                password_salt BLOB NOT NULL,
                password_hash BLOB NOT NULL,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                CHECK (username IS NOT NULL OR email IS NOT NULL)
            )
        """)

    def json_error(message, status_code):
        return jsonify({'success': False, 'message': message}), status_code

    @app.get('/api/health')
    def health():
        return jsonify({'status': 'ok', 'auth_methods': sorted(AUTH_METHODS)})

    @app.post('/api/auth/register')
    def register():
        if not LOCAL_METHODS:
            return json_error('Password sign-in is not enabled.', 403)
        data = request.get_json(silent=True)
        if not isinstance(data, dict):
            return json_error('A JSON request body is required.', 400)

        username = str(data.get('username') or '').strip() or None
        email = str(data.get('email') or '').strip().lower() or None
        password = data.get('password')
        if 'username' in LOCAL_METHODS and not username:
            return json_error('Username is required.', 400)
        if 'email' in LOCAL_METHODS and not email:
            return json_error('Email is required.', 400)
        if not isinstance(password, str) or not password:
            return json_error('Password is required.', 400)
        if 'username' not in LOCAL_METHODS:
            username = None
        if 'email' not in LOCAL_METHODS:
            email = None

        salt = secrets.token_bytes(16)
        password_hash = hashlib.pbkdf2_hmac(
            'sha256', password.encode('utf-8'), salt, PASSWORD_ROUNDS
        )
        try:
            with connect_database(app.config['AUTH_DATABASE_PATH']) as connection:
                cursor = connection.execute(
                    'INSERT INTO users (username, email, password_salt, password_hash) VALUES (?, ?, ?, ?)',
                    (username, email, salt, password_hash)
                )
                user = {
                    'id': cursor.lastrowid,
                    'username': username,
                    'email': email
                }
        except sqlite3.IntegrityError:
            return json_error('An account with those details already exists.', 409)
        return jsonify({'success': True, 'message': 'Registration successful.', 'user': user}), 201

    @app.post('/api/auth/login')
    def login():
        if not LOCAL_METHODS:
            return json_error('Password sign-in is not enabled.', 403)
        data = request.get_json(silent=True)
        if not isinstance(data, dict):
            return json_error('A JSON request body is required.', 400)

        identifier = str(data.get('username') or data.get('email') or '').strip()
        password = data.get('password')
        if not identifier or not isinstance(password, str) or not password:
            return json_error('Username/email and password are required.', 400)

        if LOCAL_METHODS == {'username', 'email'}:
            query = 'SELECT * FROM users WHERE username = ? OR email = ?'
            parameters = (identifier, identifier)
        elif 'email' in LOCAL_METHODS:
            query = 'SELECT * FROM users WHERE email = ?'
            parameters = (identifier,)
        else:
            query = 'SELECT * FROM users WHERE username = ?'
            parameters = (identifier,)

        with connect_database(app.config['AUTH_DATABASE_PATH']) as connection:
            row = connection.execute(query, parameters).fetchone()
        if row is None:
            return json_error('Invalid username/email or password.', 401)

        password_hash = hashlib.pbkdf2_hmac(
            'sha256', password.encode('utf-8'), row['password_salt'], PASSWORD_ROUNDS
        )
        if not hmac.compare_digest(password_hash, row['password_hash']):
            return json_error('Invalid username/email or password.', 401)

        user = {'id': row['id'], 'username': row['username'], 'email': row['email']}
        return jsonify({'success': True, 'message': 'Login successful.', 'user': user})

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(
        host=os.environ.get('API_HOST', '0.0.0.0'),
        port=int(os.environ.get('API_PORT', '5002')),
        debug=False
    )
