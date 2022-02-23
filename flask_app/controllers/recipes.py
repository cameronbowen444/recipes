from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models.recipe import Recipe
from flask_app.models.user import User
from flask_bcrypt import Bcrypt 
bcrypt = Bcrypt(app)

@app.route('/create')
def create():
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id" : session['user_id']
    }
    return render_template('create.html', user=User.get_id(data))

@app.route('/new_recipe', methods=['POST'])
def new():
    if 'user_id' not in session:
        return redirect('/logout')
    if not Recipe.validate_recipe(request.form):
        return redirect('/create')
    data = {
        "name": request.form["name"],
        "description": request.form["description"],
        "instructions": request.form["instructions"],
        "under30": request.form["under30"],
        "date": request.form["date"],
        "user_id": session["user_id"]
    }
    Recipe.save(data)
    return redirect('/dashboard')


@app.route('/dashboard/<int:id>')
def show_recipe(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id" : id
    }
    user_data = {
        "id":session['user_id']
    }
    return render_template("show.html", user=User.get_id(user_data), recipe=Recipe.get_one(data))

@app.route('/dashboard/edit/<int:id>')
def edit(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id" : id
    }
    user_data = {
        "id":session['user_id']
    }
    return render_template("edit.html", user=User.get_id(user_data), recipe=Recipe.get_one(data))

@app.route('/update', methods=['POST'])
def updated():
    if 'user_id' not in session:
        return redirect('/logout')
    if not Recipe.validate_recipe(request.form):
        return redirect('/dashboard/edit/<int:id>')
    data = {
        "id" : request.form['id'],
        "name" : request.form["name"],
        "description" : request.form["description"],
        "instructions" : request.form["instructions"],
        "under30" : request.form["under30"],
        "date" : request.form["date"]
    }
    Recipe.update(data)
    return redirect('/dashboard')

@app.route('/delete/<int:id>')
def destroy(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":id
    }
    Recipe.delete(data)
    return redirect('/dashboard')