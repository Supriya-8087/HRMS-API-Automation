import pytest
from controllers.user_controller import UserController
from controllers.login_controller import LoginController
import json

# read data from json file for test data instead using hardcoaded 
with open("test_data/user_data.json") as f:
    test_data = json.load(f)
with open("test_data/status_codes.json") as f:
    status_codes = json.load(f)
    print(status_codes)

token = LoginController().get_token()
user_controller = UserController(token)

def test_create_user_success():
    response = user_controller.create_user()
    response_json = response.json()
    print("✅ API Response:", response_json)

    assert response.status_code == status_codes["CREATED"], f"Expected 201 but got {response.status_code}"
    assert response_json is not None, f"❌ Empty response received!"

def test_create_user_with_empty_fields():
    response = user_controller.create_user_with_empty_fields()
    data = response.json()
    # print(data)
    assert response.status_code in {
        status_codes["BAD_REQUEST"],
        status_codes["UNPROCESSABLE_ENTITY"]
    }
    # assert "errors" in data or "message" in data


def test_create_user_with_invalid_email():
    # Invalid format (missing @)
    response = user_controller.create_user(email=test_data["invalid_email"])
    assert response.status_code == status_codes["BAD_REQUEST"]


def test_create_user_with_invalid_phone():
    # Invalid password (too short)
    response = user_controller.create_user(phone=test_data["invalid_phone"])
    # print(response)
    assert response.status_code == status_codes["BAD_REQUEST"]


def test_delete_user_with_invalid_id():
    response = user_controller.delete_user(userId=test_data["invalid_user_id"])
    # print(response)
    assert response.status_code in {
        status_codes["BAD_REQUEST"],
        status_codes["NOT_FOUND"]
    }

def test_delete_user_with_valid_id():
    response = user_controller.delete_user(userId=test_data["valid_user_id"])  # use valid id
    # print(response.status_code, response.json())
    assert response.status_code == status_codes["SUCCESS"]

def test_delete_already_deleted_user():
    response = user_controller.delete_user(userId=test_data["deleted_user_id"])  # use valid id
    # print(response.status_code, response.json())
    assert response.status_code == status_codes["BAD_REQUEST"]

def test_get_all_users():
    response = user_controller.get_all_users()
    print(response)
    assert response.status_code == status_codes["SUCCESS"]


def test_update_existing_user_status_to_inactive():
    # Use an already existing userId from DB or API
     
    update_response = user_controller.update_user_status(userId= test_data["existing_user_id"],status= "inactive")
    print("Response:", update_response.status_code, update_response.json())
    assert update_response.status_code == status_codes["SUCCESS"]

def test_update_existing_user_role():
    update_response = user_controller.update_user(userId= test_data["existing_user_id"], updates=test_data["update_user_data"])
    print(update_response.json())
    assert update_response.status_code == status_codes["SUCCESS"]

def test_update_user_manager():
    # Existing userId from DB or API 
    # Call the controller to update manager
    # values taking from json file
    update_response = user_controller.update_user_manager(userId= test_data["existing_user_id"])
    print("Response:", update_response.status_code, update_response.json())

    # Assertions
    assert update_response.status_code == status_codes["SUCCESS"]
    
    # Check if manager field is present in response