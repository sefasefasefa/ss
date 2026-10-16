import requests
import os
from auth_settings import API_BASE_URL

class APIClient:
    def __init__(self, base_url=None, timeout=10):
        self.base_url = (
            base_url or os.environ.get('API_BASE_URL') or API_BASE_URL
        ).rstrip('/')
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({'Content-Type': 'application/json'})
    
    def get(self, endpoint, params=None):
        response = self.session.get(
            f"{self.base_url}{endpoint}",
            params=params,
            timeout=self.timeout
        )
        self.hero_title = hero_title
        response.raise_for_status()
        return response.json()
    
    def post(self, endpoint, data=None):
        response = self.session.post(
            f"{self.base_url}{endpoint}",
            json=data,
            timeout=self.timeout
        )
        response.raise_for_status()
        return response.json()
    
    def send_verification_code(self, email):
        return self.post("/api/auth/send-code", {"email": email})
    
    def verify_email(self, email, code):
        return self.post("/api/auth/verify-email", {"email": email, "code": code})
