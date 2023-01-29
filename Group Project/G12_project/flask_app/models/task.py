from flask_app import app
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_bcrypt import Bcrypt
from flask_app.models import user

import re

bcrypt = Bcrypt(app)

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
DB = "taskmanager"
class Task:

    def __init__(self, task):
        self.id = task["id"]
        self.taskname = task["taskname"]
        self.created_at = task["created_at"]
        self.updated_at = task["updated_at"]
        self.user = None


    @classmethod
    def create_valid_task(cls, task_dict):
        if not cls.is_valid(task_dict):
            return False
        
        query = "INSERT INTO tasks (taskname,user_id) VALUES(%(taskname)s,%(user_id)s);"
        task_id = connectToMySQL(DB).query_db(query, task_dict)
        task = cls.get_by_id(task_id)
        return task

    @classmethod
    def get_by_id(cls,task_id):
        data = {
            "id": task_id
        }
        query = "SELECT * FROM tasks WHERE id = %(id)s;"
        result = connectToMySQL(DB).query_db(query,data)[0]
        task = cls(result)
        user_obj = user.User.get_by_id(result["user_id"])
        task.user = user_obj
        return task

    @classmethod
    def delete_task_by_id(cls, task_id):
        data = {
            "id": task_id
        }
        query = "DELETE FROM tasks WHERE ID = %(id)s;"
        connectToMySQL(DB).query_db(query, data)
        return task_id

    @classmethod
    def updated_task(cls, task_dict, session_id):
        task = cls.get_by_id(task_dict["id"])
        if task.user.id != session_id:
            flash("You cannot update this.")
            return False

        if not cls.is_valid(task_dict):
            return False
        
        query = "UPDATE tasks SET taskname = %(taskname)s WHERE id = %(id)s;"
        result = connectToMySQL(DB).query_db(query,task_dict)
        task = cls.get_by_id(task_dict["id"])
        return task

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM tasks JOIN users ON tasks.user_id=users.id"
        task_data = connectToMySQL(DB).query_db(query)
        print(task_data)
        tasks = []
        for task in task_data:
            task_obj = cls(task)
            task_obj.user= user.User(
                {
                    "id":task["user_id"],
                    "username": task["username"],
                    "firstname": task["firstname"],
                    "lastname": task["lastname"],
                    "email": task["email"],
                    "password": task["password"],
                    "created_at": task["users.created_at"],
                    "updated_at": task["users.updated_at"]
                }
            )
            tasks.append(task_obj)
        return tasks

    @staticmethod
    def is_valid(task_dict):
        valid = True
        if len(task_dict["taskname"]) < 3:
            valid = False
            flash("Task Name must be atleast 3 characters!")

        return valid