from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.api.utils import refresh, login, register, fetch_all_menu, fetch_menu, fetch_all_users, fetch_user, fetch_discounted, fetch_drinks, profile


class Login(Resource):
    def post(self):
        response = login()
        return response
    
class Refresh(Resource):
    @jwt_required(refresh=True)
    def post(self):
        response = refresh()
        return response

class Registration(Resource):
    def post(self):
        response = register()
        return response
    
class AllUsers(Resource):
    @jwt_required()
    def get(self):
        response = fetch_all_users()
        return response
    
class FetchUser(Resource):
    @jwt_required()
    def get(self):
        response = fetch_user()
        return response


class FetchAll(Resource):
    @jwt_required()
    def get(self):
        response = fetch_all_menu() 
        return response

class FetchOne(Resource):
    def get(self):
        response = fetch_menu()
        return response

class Profile(Resource):
    def get(self):
        response = profile()
        return response
    
class FetchDrinks(Resource):
    def get(self):
        response = fetch_drinks()
        return response
    

class Discounted(Resource):
    def get(self):
        response = fetch_discounted()
        return response
    