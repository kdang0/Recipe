from flask_app import app
from flask_app.models.recipe import Recipe
from flask import redirect, request, session, render_template, flash
from flask_app.models.user import User

@app.route('/recipes/new')
def add_recipe():
    return render_template("add.html")

@app.route('/create', methods = ["POST"])
def add():

    if not Recipe.validate_recipe(request.form):
        return redirect('/recipes/new')
    data = {
        'user_id' : session["user_id"],
        **request.form
    }
    Recipe.save(data)
    return redirect('/dashboard')

@app.route('/edit/<int:id>', methods= ["POST"])
def edit(id):
    data = {
        "id" : id,
        **request.form
    }
    Recipe.update(data)
    return redirect('/dashboard')

@app.route('/delete/<int:id>')
def delete(id):
    data = {
        "id" : id
    }
    Recipe.delete(data)
    return redirect('/dashboard')

@app.route('/recipes/<int:id>')
def show_recipe(id):
    data = {
        "id" : id
    }
    user_data = { "id" : session['user_id']}
    user = User.get_cur_user(user_data)
    recipe = Recipe.get_one(data)
    user_recipe = User.get_cur_user({"id" : recipe["id"]})
    return render_template('show.html', user=user, recipe = recipe["recipe"], user_recipe=user_recipe)

@app.route('/recipes/edit/<int:id>')
def edit_recipe(id):
    data = {
        "id" : id
    }
    user_data = { "id" : session['user_id']}
    user = User.get_cur_user(user_data)
    recipe = Recipe.get_one(data)
    print(recipe["recipe"].id)
    user_recipe = User.get_cur_user({"id" : recipe["id"]})
    return render_template('edit.html', user=user, recipe = recipe["recipe"], user_recipe=user_recipe)


