from flask_app.models.task import Task
from flask import Flask, render_template, session, redirect, request
from flask_app import app
from flask_app.models.user import User
from flask_app.models.task import Task
from flask_app.models.comment import Comment
from flask import flash

@app.route('/comment/<int:task_id>', methods=['POST'])
def comment_on_task(task_id):
    data = {
        "tip": request.form['tip'],
        "task_id": request.form['task_id'],
        "user_id": request.form['user_id']
        }
            
    Comment.save(data)
    return redirect(f"/task/{task_id}")

    # need delete route