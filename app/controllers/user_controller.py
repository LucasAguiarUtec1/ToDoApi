from flask import abort, jsonify, request
from app.services.user_service import UserService
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()

class UserController:
    @staticmethod
    def get_users():
        users = UserService.get_all_users()
        return users, 200
   
    @staticmethod
    def create_user():
        data = request.json
        username = data['username']
        email = data['email']
        password = data ['password']

        if not username or not email or not password:
            abort(400, 'Username, email and password are required')
        
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        try:
            return UserService.create_user(username=username, email=email, password=hashed_password), 200
        except ValueError as e:
            raise
        except Exception as e:
            abort(500, description='Internal server error')
    
    @staticmethod
    def delete_user(id):
        if not id:
            raise ValueError('Bad request')

        try:
            UserService.delete_user(id)
            return '', 204
        except ValueError as e:
            raise
        except Exception as e:
            abort(500, description='Internal server error')

    @staticmethod
    def update_user(id):
        data = request.json
        username = data['username']
        email = data['email']
        if not id:
            raise ValueError('Bad request')
        
        try:
            UserService.update_user(id, username=username, email=email)
            return '', 204
        except ValueError:
            raise
        except Exception as e:
            abort(500, description='Internal server error')