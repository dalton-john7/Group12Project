from flask_app import app
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_bcrypt import Bcrypt
from flask_app.models import user,task
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

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM comments;"
        results = connectToMySQL(DB).query_db(query)
        tasks = []

        for task in results:
            tasks.append(cls(task))
            return tasks

    

    @classmethod
    def save(cls, data):
        query = "INSERT INTO comments (tip, task_id) VALUES(%(tip)s,%(task_id)s;"
        return connectToMySQL(DB).query_db(query,data)

# need delete method