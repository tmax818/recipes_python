import flask_app
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import flash
from pprint import pprint
import re  # the regex module

# create a regular expression object that we'll use later
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
from flask_app.models.recipe import Recipe

DATABASE = 'recipes'


class User:

    def __init__(self, data) -> None:
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.recipes = []
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    # ! CREATE
    @classmethod
    def save(cls, data):
        query = "INSERT INTO users (first_name, last_name, email, password) VALUES (%(first_name)s,%(last_name)s,%(email)s,%(password)s);"
        return connectToMySQL(DATABASE).query_db(query, data)

    # ! READ ONE FROM EMAIL
    @classmethod
    def get_by_email(cls, data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        result = connectToMySQL(DATABASE).query_db(query, data)
        if len(result) > 0:
            return User(result[0])
        else:
            return False

    @classmethod
    def get_one_with_recipes(cls, data):

        query = "SELECT * FROM users LEFT JOIN recipes ON users.id = recipes.user_id WHERE users.id= %(id)s;"
        results = connectToMySQL(DATABASE).query_db(query, data)
        pprint(results)
        user = User(results[0])
        print(user.recipes)
        for result in results:
            temp_recipe = {
                "id": result['recipes.id'],
                "name": result['name'],
                "description": result['description'],
                "instructions": result['instructions'],
                "date_made": result['date_made'],
                "under_30": result['under_30'],
                "user_id": result['user_id'],
                "created_at": result['recipes.created_at'],
                "updated_at": result['recipes.updated_at']
            }
            user.recipes.append(Recipe(temp_recipe))
        print(user.recipes)

        return user

    @staticmethod
    def validate_user(user):
        is_valid = True
        if len(user['first_name']) < 2:
            is_valid = False
            flash("Sorry, use at least 2 chars")
        if not EMAIL_REGEX.match(user['email']):
            flash("Invalid email address!")
            is_valid = False
        return is_valid