from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import user

class Show:
    def __init__(self,data):
        self.id = data['id']
        self.title = data['title']
        self.network = data['network']
        self.description = data['description']
        self.release_date = data['release_date']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.userself = None

    @classmethod
    def create(cls, data):
        query = "INSERT INTO tv_shows (title, network, description, release_date, user_id) VALUES (%(title)s, %(network)s, %(description)s, %(release_date)s, %(user_id)s);"
        results = connectToMySQL('login_registration').query_db(query,data)
        print (results)
        return results

    @classmethod
    def get_users_and_shows(cls):
        query = "SELECT * FROM tv_shows JOIN users on users.id = tv_shows.user_id;"
        results = connectToMySQL('login_registration').query_db(query)
        print (results)
        all_shows = []

        for pho in results:
            one_show = cls(pho)
            user_data ={
                'id':pho['users.id'], 
                'first_name':pho['first_name'],
                'last_name':pho['last_name'],
                'email':pho['email'],
                'password':None,
                'created_at': pho['users.created_at'],
                'updated_at':pho['users.updated_at']
            }
            user_obj = user.User(user_data)
            one_show.userself = user_obj
            all_shows.append(one_show)
        return all_shows

    @classmethod
    def destroy (cls, data):
        query = "DELETE FROM tv_shows WHERE id = %(id)s;"
        return connectToMySQL('login_registration').query_db(query, data)

    @classmethod
    def get_description (cls, data):
        query = "SELECT * FROM tv_shows JOIN users on users.id = tv_shows.user_id WHERE tv_shows.id = %(id)s;"
        result = connectToMySQL('login_registration').query_db(query, data)

        row = cls (result[0])

        one_user_data={
            'id':result[0]['users.id'],
            'first_name':result[0]['first_name'],
            'last_name':result[0]['last_name'],
            'email':result[0]['email'],
            'password': None,
            'created_at':result[0]['users.created_at'],
            'updated_at':result[0]['users.updated_at']
        }
        user_obj=user.User(one_user_data)
        row.userself = user_obj
        return row

    @classmethod
    def get_one(cls,data):
        query  = "SELECT * FROM tv_shows WHERE id = %(id)s;"
        result = connectToMySQL('login_registration').query_db(query,data)
        return cls(result[0])

    @classmethod
    def update(cls,data):
        query = "UPDATE tv_shows SET title=%(title)s,network=%(network)s,description=%(description)s,updated_at=NOW() WHERE id = %(id)s;"
        return connectToMySQL('login_registration').query_db(query,data)


    @staticmethod
    def validate_register(tv):
        is_valid = True # we assume this is true
        if len(tv['title']) < 3:
            flash("Title must be at least 3 characters")
            is_valid= False
        if len(tv['network']) < 3:
            flash("Network must be at least 3 characters")
            is_valid= False
        if len(tv['description']) < 3:
            flash("Description must be at least 3 characters")
            is_valid= False
        return is_valid