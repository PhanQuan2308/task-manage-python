from pymongo import MongoClient
from werkzeug.security import check_password_hash, generate_password_hash

from config import Config

client = MongoClient(Config.MONGO_URI)
db = client['task_management']
users = db['users']

class User:
    @staticmethod
    def create_user(username, password):
        hashed_password = generate_password_hash(password)
        users.insert_one({'username': username, 'password': hashed_password})

    @staticmethod
    def find_by_username(username):
        return users.find_one({'username': username})

    @staticmethod
    def verify_password(username, password):
        user = User.find_by_username(username)
        if user and check_password_hash(user['password'], password):
            return user
        return None
