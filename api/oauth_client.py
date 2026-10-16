import secrets
import sys
import time
import webbrowser
from urllib.parse import quote

import requests

class OAuthLoginClient:
    def __init__(self, server_url):
        self.server_url = server_url.rstrip('/')

    def start(self, provider):
        flow_id = secrets.token_urlsafe(32)
        login_url = (
            f"{self.server_url}/auth/{quote(provider)}/start/{quote(flow_id)}"
        )
        self._open_login_page(login_url)
        return flow_id

    @staticmethod
    def _open_login_page(login_url):
        if sys.platform == 'android':
            try:
                from jnius import autoclass
                activity = autoclass('org.kivy.android.PythonActivity').mActivity
                intent = autoclass('android.content.Intent')(
                    autoclass('android.content.Intent').ACTION_VIEW,
                    autoclass('android.net.Uri').parse(login_url)
                )
                activity.startActivity(intent)
            except (ImportError, AttributeError, RuntimeError) as error:
                raise RuntimeError("Could not open the system browser on Android.") from error
            return
        if sys.platform == 'ios':
            try:
                from pyobjus import autoclass
                app = autoclass('UIApplication').sharedApplication()
                url = autoclass('NSURL').URLWithString_(login_url)
                app.openURL_(url)
            except (ImportError, AttributeError, RuntimeError) as error:
                raise RuntimeError("Could not open the system browser on iOS.") from error
            return
        if not webbrowser.open(login_url):
            raise RuntimeError("Could not open the OAuth sign-in page.")

    def wait_for_login(self, flow_id, timeout=180):
        deadline = time.monotonic() + timeout
        while time.monotonic() < deadline:
            response = requests.get(
                f"{self.server_url}/api/auth/poll/{quote(flow_id)}",
                timeout=10
            )
            response.raise_for_status()
            result = response.json()
            if result.get('status') == 'complete':
                return result
            if result.get('status') == 'failed':
                raise RuntimeError(result.get('error', 'OAuth sign-in failed.'))
            time.sleep(1)
        raise TimeoutError("OAuth sign-in timed out.")

    def authenticate(self, provider, timeout=180):
        return self.wait_for_login(self.start(provider), timeout)
