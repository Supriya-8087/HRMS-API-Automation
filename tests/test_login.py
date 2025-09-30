import pytest
from controllers.login_controller import LoginController
from utils.db_config import DBClient
import json

with open("test_data/status_codes.json") as f:
    test_data = json.load(f)  
login = LoginController()


def test_login_success():
    token = login.get_token()   # Directly gets token

    assert token is not None, "Token should not be None"
    print(f"✅ Login successful, token received: {token}")

def test_login_response_code():
    response = login.login()
    assert response.status_code == test_data["SUCCESS"]


def test_login_contains_token():
    response = login.login()
    assert "authToken" in response.json().get("data", {})

#negative flow

def test_login_invalid_username():
    response = login.login_invalid_username()
    response_json = response.json()
    print(response_json)
    assert response.status_code in{
        test_data["BAD_REQUEST"],
        test_data["UNAUTHORIZED"]
    } 
    
def test_login_invalid_password():
    response = login.login_invalid_password()
    assert response.status_code in{
        test_data["BAD_REQUEST"],
        test_data["UNAUTHORIZED"]
    }

def test_login_missing_username():
    response = login.login_missing_username()
    assert response.status_code in{
        test_data["BAD_REQUEST"],
        test_data["UNAUTHORIZED"]
    }

def test_login_missing_password():
    response = login.login_missing_password()
    assert response.status_code in{
        test_data["BAD_REQUEST"],
        test_data["UNAUTHORIZED"]
    }

def test_login_empty_payload():
    response = login.login_empty_payload()
    assert response.status_code in{
        test_data["BAD_REQUEST"],
        test_data["UNAUTHORIZED"]
    }

def test_login_sql_injection():
    response = login.login_sql_injection()
    assert response.status_code in{
        test_data["BAD_REQUEST"],
        test_data["UNAUTHORIZED"]
    }