import pytest
from controllers.user_controller import UserController
from controllers.login_controller import LoginController

token = LoginController().get_token()
user_controller = UserController(token)

def test_create_user_success():
    response = user_controller.create_user()
    response_json = response.json()
    print("✅ API Response:", response_json)

    assert response.status_code == 201, f"Expected 201 but got {response.status_code}"
    assert response_json is not None, f"❌ Empty response received!"

def test_create_user_with_empty_fields():
    response = user_controller.create_user_with_empty_fields()
    data = response.json()
    # print(data)
    assert response.status_code in [400, 422]
    # assert "errors" in data or "message" in data


def test_create_user_with_invalid_email():
    # Invalid format (missing @)
    response = user_controller.create_user(email="supriya.mgmail.com")
    assert response.status_code == 400


def test_create_user_with_invalid_phone():
    # Invalid password (too short)
    response = user_controller.create_user(phone="12345")
    # print(response)
    assert response.status_code == 400


def test_delete_user_with_invalid_id():
    response = user_controller.delete_user(userId="12345")
    # print(response)
    assert response.status_code in [400,404]

def test_delete_user_with_valid_id():
    response = user_controller.delete_user(userId="68d0f1a7dff3a925158a3e89")  # use valid id
    # print(response.status_code, response.json())
    assert response.status_code == 200

def test_delete_already_deleted_user():
    response = user_controller.delete_user(userId="68d0d5da88c876179efb53af")  # use valid id
    # print(response.status_code, response.json())
    assert response.status_code == 400

def test_get_all_users():
    response = user_controller.get_all_users()
    print(response)
    assert response.status_code == 200


def test_update_existing_user_status_to_inactive():
    # Use an already existing userId from DB or API
    existing_user_id = "68d0f1a7dff3a925158a3e89"  
    update_response = user_controller.update_user_status(existing_user_id, "inactive")
    print("Response:", update_response.status_code, update_response.json())
    assert update_response.status_code == 200

def test_update_existing_user_role():
    exe_user_id = "68d0f1a7dff3a925158a3e89"
    updates ={"status": "active", "role": "Recruiter", "fName": "John"}
    update_response = user_controller.update_user(userId= exe_user_id, updates=updates)
    print(update_response.json())
    assert update_response.status_code == 200

def test_update_user_manager():
    # Existing userId from DB or API
    existing_user_id = "68d0f1a7dff3a925158a3e89"  # replace with a real userId

    # Call the controller to update manager
    update_response = user_controller.update_user_manager(userId=existing_user_id)
    print("Response:", update_response.status_code, update_response.json())

    # Assertions
    assert update_response.status_code == 200
    # Check if manager field is present in response
    

