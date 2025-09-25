import requests
import random
import string
from config.env import Env
from config.endpoints import Endpoints
from config.db_helper import DBHelper


class UserController:
    def __init__(self, token):
        self.session = requests.Session()
        self.session.headers.update({
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}"
        })
        self.db = DBHelper()

    # 🔹 Helper: generate random email
    def _generate_random_email(self):
        random_str = ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))
        return f"user_{random_str}@gmail.com"

    # 🔹 Helper: generate random phone
    def _generate_random_phone(self):
        return int("9" + "".join(random.choices("0123456789", k=9)))  # always 10 digits starting with 9

    def build_user_payload(self, email=None, phone=None):
        """Build user payload with dynamic IDs from DB"""
        dept_id = self.db.get_department_id()
        role_id = self.db.get_role_id()
        manager_ids = self.db.get_user_id_by_department("Testing")
        #choose single id that's why use random.choice function here 
        manager_id = random.choice(manager_ids) if manager_ids else None
        # manager_id = DBHelper.get_reporting_manager("Testing")

        return {
            "fName": "Postman",
            "lName": "Testing",
            "email": email or self._generate_random_email(),
            "phone": phone or self._generate_random_phone(),
            "password": "Test@123",
            "roleId": role_id,
            "departmentId": dept_id,
            "reportingManagerId": manager_id,
            "emailVerify": True,
            "phoneVerify": True
        }

    def create_user(self, email=None, phone=None):
        """Creates a user with valid payload"""
        payload = self.build_user_payload(email, phone)
        return self._send_create_request(payload)

    def create_user_with_empty_fields(self):
        payload = {
            "fName": "",
            "lName": "",
            "email": "",
            "phone": "",
            "password": "",
            "roleId": "",
            "departmentId": "",
            "reportingManagerId": ""
        }
        return self._send_create_request(payload)

    # 🔹 Private reusable request sender
    def _send_create_request(self, payload):
        response = self.session.post(
            f"{Env.BASE_URL()}{Endpoints.CREATE_USER}",
            json=payload
        )
        return response

    def delete_user(self, userId):
        payload = {"userId": userId}   # must match API
        response = self.session.delete(
            f"{Env.BASE_URL()}{Endpoints.DELETE_USER}",
            json=payload
        )
        return response

    def get_all_users(self):
        """
        Fetch all users.
        """
        return self.session.get(
            f"{Env.BASE_URL()}{Endpoints.GET_USERS}"
        )

    def update_user(self, userId, updates: dict):
        """
        Update a user by ID with any fields.
        Example: {"status": "Inactive"} or {"fName": "NewName"}
        """
        payload = {"userId": userId, **updates}
        response = self.session.patch(
            f"{Env.BASE_URL()}{Endpoints.UPDATE_USER}",
            json=payload
        )
        return response

    def update_user_status(self, userId, status: str):
        """
        Update only the user's status (Active/Inactive).
        """
        payload = {"userId": userId, "status": status}
        response = self.session.patch(
            f"{Env.BASE_URL()}{Endpoints.UPDATE_USER}",
            json=payload
        )
        return response
    
    def update_user_manager(self, userId):
        manager_ids = self.db.get_user_id_by_department("Testing")
        manager_id = random.choice(manager_ids) if manager_ids else None
        print(manager_id)
        payload = {"userId": userId, "reportingManagerId": manager_id}
        response = self.session.patch(
            f"{Env.BASE_URL()}{Endpoints.UPDATE_USER}",
            json=payload
        )
        return response
