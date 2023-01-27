from flask_app.config.mysqlconnection import connectToMySQL
from .comment import Comment

DB = "taskmanager"

class Task:
    def __init__( self , data ):
        self.id = data['id']
        self.name = data['name']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.comments = []

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM tasks;"
        results = connectToMySQL(DB).query_db(query)
        tasks = []

        for task in results:
            tasks.append(cls(task))
            return tasks

    @classmethod
    def get_one_task_with_comments(cls,data):
        query = "SELECT * FROM tasks LEFT JOIN comments on tasks.id = comments.task_id WHERE tasks.id = %(id)s;"

        results = connectToMySQL(DB).query_db(query,data)
        task = cls(results[0])
        for row in results:
            n = {
                'id': row['comments.id'],
                'tip': row['tip'],
                'created_at': row['comments.created_at'],
                'updated_at': row['comments.updated_at']
            }
            task.comments.append(Comment(n))
        return task


    @classmethod
    def save(cls, data):
        query = "INSERT INTO tasks (name, created_at, updated_at ) VALUES(%(name)s,NOW(),NOW());"
        return connectToMySQL(DB).query_db(query,data)

    @classmethod
    def edit_task(cls,data):
        query = "UPDATE tasks SET name = %(name), updated_at=NOW() WHERE id = %(id)s;"
        return connectToMySQL(DB).query_db(query,data)

    @classmethod
    def delete_task(cls,data):
        query = "DELETE FROM tasks WHERE id = %(id)s"
        return connectToMySQL(DB).query_db(query,data)