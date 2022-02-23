from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re 
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 

class Recipe:
    db = "recipe"
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.description = data['description']
        self.instructions = data['Instructions']
        self.date = data['date']
        self.under30 = data['under30']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.creator = None
        
    
    @classmethod 
    def save(cls, data):
        query = "INSERT INTO recipe (name, description, instructions, date, under30, user_id, created_at, updated_at) VALUES (%(name)s, %(description)s, %(instructions)s, %(date)s, %(under30)s, %(user_id)s, NOW(), NOW());"
        return connectToMySQL(cls.db).query_db(query, data)


    @staticmethod
    def validate_recipe(recipe):
        is_valid = True
        if len(recipe['name']) < 3:
            flash("name must be at least 3 characters")
            is_valid = False
        if len(recipe['description']) < 3:
            flash("description must be at least 3 characters")
            is_valid = False
        if len(recipe['instructions']) < 3:
            flash("instructions must be at least 3 characters")
            is_valid = False
        if recipe['date'] == "":
            flash("date must be filled out")
            is_valid = False
        return is_valid

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM recipe;"
        results = connectToMySQL(cls.db).query_db(query)
        all_recipes = []
        
        for row in results:
            all_recipes.append(cls(row))
        return all_recipes

    @classmethod 
    def get_one(cls, data):
        query = "SELECT * FROM recipe WHERE id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query, data)

        recipes = []

        for row in results:
            recipes.append(cls(row))
        return recipes
    

    @classmethod
    def update(cls, data):
        query = "UPDATE recipe SET name=%(name)s, description=%(description)s, instructions=%(instructions)s, date=%(date)s, under30=%(under30)s, updated_at=NOW() WHERE id = %(id)s;"
        
        return connectToMySQL(cls.db).query_db(query, data)

    @classmethod
    def delete(cls, data):
        query = "DELETE FROM recipe WHERE id = %(id)s;"
        return connectToMySQL(cls.db).query_db(query, data)