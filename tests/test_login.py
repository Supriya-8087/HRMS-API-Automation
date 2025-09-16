import pytest
from controllers.login_controller import LoginController
from config.db_config import DBClient
import json

@pytest.mark.smoke
def test_login_success():
    login = LoginController()
    token = login.get_token()   # Directly gets token

    assert token is not None, "Token should not be None"
    print(f"✅ Login successful, token received: {token}")



