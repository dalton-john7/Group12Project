from flask_app import app
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import task
from flask_app.models import user
from flask_bcrypt import Bcrypt
import re

bcrypt = Bcrypt(app)

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')


DB = "taskmanager"
class Comment:
    def __init__( self , data ):
        self.id = data['id']
        self.tip = data['tip']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user=None
        self.task=None

    @classmethod
    def get_all(cls, data):
        query = "SELECT * FROM tasks LEFT JOIN comments ON comments.task_id = tasks.id JOIN users ON users.id = comments.user_id WHERE comments.task_id = %(id)s;"
        results = connectToMySQL(DB).query_db(query, data)
        
        comments = []
        for comment in results:
            comment_data = cls(comment)
            comment_data.task= task.Task
            comment_data.user = user.User(
                {   
                    'id':comment["task_id"],
                    'tip':comment["tip"],
                    'username': comment["username"],
                    'firstname':comment["firstname"],
                    'lastname':comment["lastname"],
                    'email':comment["email"],
                    'password':comment["password"],
                    'taskname':comment["taskname"],
                    "created_at": comment["created_at"],
                    "updated_at": comment["updated_at"]
                }
            )
            
            print(comment["username"])
            comments.append(comment_data)
        return comments
#Commenting this method for now - will be working on the above
    # @classmethod
    # def get_comments_for_task(cls, task_id):
    #     data = {
    #         "id": task_id
    #     }
    #     query = "select firstname, lastname, tip, user_id from comments join users on comments.user_id = users.id where comments.task_id = %(id)s;"
    #     results = connectToMySQL(DB).query_db(query)
    #     comments = []

    #     for comment in results:
    #         task_obj = cls(comment)
    #         task_obj.task = task.Task(
    #             {
    #                 "id":comment['user_id'],
    #                 "tip":comment['tip'],
    #                 "firstname":comment['firstname'],
    #                 "lastname":comment['lastname']
    #             }
    #         )

    #         comments.append(task_obj)
    #     return comments

        return 
    @classmethod
    def save(cls, data):
        query = "INSERT INTO comments (tip, task_id, user_id) VALUES(%(tip)s,%(task_id)s,%(user_id)s);"
        return connectToMySQL(DB).query_db(query,data)

# need delete method