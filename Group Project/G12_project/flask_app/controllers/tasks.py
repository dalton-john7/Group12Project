from flask import Flask, render_template, session, redirect, request
from flask_app import app
from flask_app.models.user import User
from flask_app.models.task import Task
from flask import flash

@app.route("/tasks/home")
def tasks_home():
    if "user_id" not in session:
        flash("Login to access dashboard")
        return redirect("/")
    user = User.get_by_id(session["user_id"])
    task = Task.get_all()

    return render_template("home.html", user=user, task=task)


@app.route("/task/<int:task_id>")
def task_detail(task_id):
    user = User.get_by_id(session["user_id"])
    task = Task.get_by_id(task_id)
    return render_template("task_detail.html", user=user, task=task)


@app.route("/task/create")
def task_create_page():
    user = User.get_by_id(session["user_id"])
    return render_template("create_task.html", user=user)


@app.route("/task/edit/<int:task_id>")
def task_edit_page(task_id):
    task = Task.get_by_id(task_id)
    return render_template("edit_task.html", task=task)


@app.route("/tasks", methods=["POST"])
def create_task():
    valid_task = Task.create_valid_task(request.form)
    if valid_task:
        return redirect(f"/task/{valid_task.id}")
    return redirect("/task/create")


@app.route("/task/<int:task_id>", methods=["POST"])
def update_task(task_id):
    valid_task = Task.updated_task(request.form, session["user_id"])
    if not valid_task:
        return redirect (f"/task/edit/{task_id}")
    return redirect(f"/task/{task_id}")


@app.route("/task/delete/<int:task_id>")
def delete_by_id(task_id):
    Task.delete_task_by_id(task_id)
    return redirect("/tasks/home")