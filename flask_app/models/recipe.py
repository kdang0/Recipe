from flask_app.config.mysqlconnection import connectToMySQL
from flask import session, flash

class Recipe:
    def __init__(self, data):
        self.id = data["id"]
        self.name = data["name"]
        self.description = data["description"]
        self.date_cooked = data["date_cooked"]
        self.instruction = data["instruction"]
        self.is_under_thirty = data["is_under_thirty"]

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM recipes;"
        recipes = []
        results = connectToMySQL('recipe_schema').query_db(query)
        if results:
            for recipe in results:
                recipes.append(cls(recipe))
            return recipes
    
    @classmethod
    def save(cls, data):
        query = "INSERT INTO recipes (user_id, name, is_under_thirty, instruction, description, date_cooked) "
        query += "VALUES(%(user_id)s, %(name)s, %(is_under_thirty)s, %(instruction)s, %(description)s, %(date_cooked)s);"
        return connectToMySQL('recipe_schema').query_db(query, data)
    
    @classmethod
    def get_one(cls,data):
        query = "SELECT * FROM recipes WHERE "
        query += "id = %(id)s;"
        result = connectToMySQL('recipe_schema').query_db(query, data)
        if result:
            recipe = cls(result[0])
            recipe_data = {
                "recipe" : recipe,
                "id" : result[0]["user_id"]
            }
            return recipe_data
    

    @classmethod
    def delete(cls,data):
        query = "DELETE FROM recipes WHERE id = %(id)s;"
        return connectToMySQL('recipe_schema').query_db(query, data)

    @classmethod
    def update(cls, data):
        query = "UPDATE recipes SET "
        query += "name=%(name)s, date_cooked=%(date_cooked)s, description=%(description)s, instruction=%(instruction)s, is_under_thirty = %(is_under_thirty)s "
        query += "WHERE id = %(id)s;"
        return connectToMySQL('recipe_schema').query_db(query, data)
    
    @staticmethod
    def validate_recipe(recipe):
        is_valid = True
        if len(recipe["name"]) < 3:
            flash("Name needs to be at least 3 characters")
            is_valid = False
        if len(recipe["description"]) < 3:
            flash("Description needs to be at least 3 characters")
            is_valid = False
        if len(recipe["instruction"]) < 3: 
            flash("Instruction must be at least 3 characters")
            is_valid = False
        if recipe["date_cooked"] is None:
            flash("Please enter date")
            is_valid = False
        if "is_under_thirty" not in recipe or recipe['under_thirty'] not in ['0', '1']:
            flash("Please check whether the recipe is under thirty minutes")
            is_valid = False
        return is_valid