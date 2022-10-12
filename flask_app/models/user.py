from flask_app.config.mysqlconnection import connectToMySQL
from flask import session, flash
import re
from flask_app import bcrypt
from flask_app.models import recipe
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 
class User:
    def __init__(self, data):
        self.id = data["id"]
        self.first_name = data["first_name"]
        self.last_name = data["last_name"]
        self.email = data["email"]
        self.password = data["password"]
        self.recipes = []


    @classmethod
    def get_cur_user(cls, data):
        query = "SELECT * FROM users WHERE"
        query += ' AND'.join(f' {key} = %({key})s' for key in data)
        query += ";"
        user = connectToMySQL('recipe_schema').query_db(query, data)
        if user:
            return cls(user[0])
    @classmethod
    def save(cls, data):
        data['password'] = bcrypt.generate_password_hash(data["password"])
        query = "INSERT INTO users (first_name, email, last_name, password)"
        query += " VALUES(%(first_name)s, %(email)s, %(last_name)s, %(password)s)"

        return connectToMySQL('recipe_schema').query_db(query,data)
    
    @classmethod
    def users_w_recipes(cls):
        query = "SELECT * FROM users JOIN recipes ON "
        query += "users.id = recipes.user_id;"
        results = connectToMySQL('recipe_schema').query_db(query)
        user_recipes = []
        print(results)
        if results:
            for row_db in results:
                user_data = {
                    "first_name" : row_db["first_name"],
                    "id" : row_db["user_id"]
                }
                recipe_data = {
                    "id" : row_db["recipes.id"],
                    "date_cooked" : row_db["date_cooked"],
                    "description" : row_db["description"],
                    "instruction" : row_db["instruction"],
                    "is_under_thirty" : row_db["is_under_thirty"],
                    "name" : row_db["name"]
                }
                a_recipe = recipe.Recipe(recipe_data)
                recipe_information = {
                    "recipe" : a_recipe,
                    "user" : user_data
                }
                print(recipe_information)
                user_recipes.append(recipe_information)
            print(user_recipes)
            return user_recipes

    @staticmethod
    def validate_registration(user):
        is_valid = True
        if len(user["first_name"]) < 2 and not user["first_name"].isalpha():
            flash("Invalid firstname")
            is_valid = False
        if len(user["last_name"]) < 2 and not user["last_name"].isalpha():
            flash("Invalid lastname")
            is_valid = False
        if not EMAIL_REGEX.match(user["email"]):
            flash("Invalid email address")
            is_valid = False

        results = User.get_cur_user({"email" : user["email"]})
        if results:
            flash("This email is already taken")
            is_valid = False
        if len(user['password']) < 8:
            flash("Invalid password")
            is_valid = False
        if user['password'] != user['confirm_password']:
            flash("Password's don't match")
            is_valid = False

        return is_valid
    
    @staticmethod
    def validate_login(data):
        
        user_in_db = User.get_cur_user({"email" : data["email"]})
        if not user_in_db:
            flash("Invalid Email/Password")
            return False
        if not bcrypt.check_password_hash(user_in_db.password, data['password']):
            flash("Invalid Email/Password")
            return False
        return True