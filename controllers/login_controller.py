import requests
from config.env import Env
from config.endpoints import Endpoints

class LoginController:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            "Content-Type": "application/json"
        })

    def login(self):
        """Performs login and returns full response"""
        payload = {
            "username": Env.USERNAME(),
            "password": Env.PASSWORD()
        }
        response = self.session.post(
            f"{Env.BASE_URL()}{Endpoints.LOGIN}",
            json=payload
        )
        return response

    def get_token(self):
        """Helper: Logs in and extracts auth token"""
        response = self.login()
        if response.status_code != 200:
            raise Exception(f"Login failed with status {response.status_code}, body: {response.text}")
        
        json_data = response.json()
        token = json_data.get("data", {}).get("authToken")
        if not token:
            raise Exception("authToken not found in response")
        return token
