from bson.objectid import ObjectId
from pymongo import MongoClient

from config import Config

client = MongoClient(Config.MONGO_URI)
db = client["task_management"]
tasks = db["tasks"]


class Task:
    @staticmethod
    def create_task(user_id, name, description, deadline, priority):
        task = {
            "user_id": user_id,
            "name": name,
            "description": description,
            "deadline": deadline,
            "priority": priority,
            "completed": False,
        }
        tasks.insert_one(task)

    @staticmethod
    def get_user_tasks(user_id):
        user_tasks = list(tasks.find({"user_id": user_id}))
        for task in user_tasks:
            task["_id"] = str(task["_id"])
        return user_tasks

    @staticmethod
    def get_task_by_id_and_user(task_id, user_id):

        task = tasks.find_one({"_id": ObjectId(task_id), "user_id": user_id})
        if task:
            task["_id"] = str(task["_id"])
        return task

    @staticmethod
    def update_task(task_id, user_id, data):
        result = tasks.update_one({"_id": ObjectId(task_id), "user_id": user_id}, {"$set": data})
        return result.matched_count > 0

    @staticmethod
    def delete_task(task_id, user_id):
        result = tasks.delete_one({"_id": ObjectId(task_id), "user_id": user_id})
        return result.deleted_count > 0
    @staticmethod
    def toggle_task_completion(task_id, user_id):
        task = tasks.find_one({"_id": ObjectId(task_id), "user_id": user_id})
        if task:
            new_status = not task.get("completed", False)
            tasks.update_one(
                {"_id": ObjectId(task_id), "user_id": user_id},
                {"$set": {"completed": new_status}}
            )
            return new_status
        return None