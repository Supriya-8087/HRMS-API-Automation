import requests
from config.env import Env
from config.endpoints import Endpoints

class LoginController:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            "Content-Type": "application/json"
        })

    def login(self,username=None, password=None):
        """Performs login and returns full response"""
        payload = {
            "username": username or Env.USERNAME(),
            "password": password or Env.PASSWORD()
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

    def login_valid_data(self):
        return self.login(username=Env.USERNAME, password=Env.PASSWORD)
    
    def login_invalid_username(self):
        return self.login(username="abc@gmail.com", password=Env.PASSWORD())

    def login_invalid_password(self):
        return self.login(username=Env.USERNAME(), password="wrong_pass")

    def login_missing_username(self):
        return self.session.post(f"{Env.BASE_URL()}{Endpoints.LOGIN}", json={"password": Env.PASSWORD()})

    def login_missing_password(self):
        return self.session.post(f"{Env.BASE_URL()}{Endpoints.LOGIN}", json={"username": Env.USERNAME()})

    def login_empty_payload(self):
        return self.session.post(f"{Env.BASE_URL()}{Endpoints.LOGIN}", json={})

    def login_sql_injection(self):
        return self.login(username="' OR 1=1 --", password="anything")