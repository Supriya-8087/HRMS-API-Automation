from config.db_config import DBClient
from bson import ObjectId


class DBHelper:
    def __init__(self):
        self.db = DBClient()

    def get_role_id(self, role_name="employee"):
        role = self.db.get_collection("role").find_one({"name": role_name})
        return str(role["_id"]) if role else None

    def get_department_id(self, dept_name="Testing"):
        dept = self.db.get_collection("department").find_one({"name": dept_name})
        return str(dept["_id"]) if dept else None

    #reporting manager 
    def get_user_id_by_department(self, dept_name="Testing"):
        """
        Get first user's _id from users collection
        where departmentId matches the given department name.
        """
        # Step 1: Get the department ID
        dept_id = self.get_department_id(dept_name)
        if not dept_id:
            return None
        # Mongo won’t match ObjectId("68747061e768e76c83be2a87") with the string "68747061e768e76c83be2a87 so that's why use ObjectId".
        users_cursor = self.db.get_collection("users").find({"departmentId": ObjectId(dept_id)})
        user_ids = [str(user["_id"]) for user in users_cursor]
        return user_ids
    
    