from flask import abort, jsonify, request
from app.services.user_service import UserService
from app.controllers.blocklist_controller import BlocklistController
from flask_bcrypt import Bcrypt
from flask_jwt_extended import create_access_token, jwt_required, decode_token

bcrypt = Bcrypt()

class UserController:
    @staticmethod
    def login():
        data = request.get_json(silent=True)
        if not data:
            abort(400, 'request must be JSON')
        
        email = data.get('email')
        password = data.get('password')

        if email is None or password is None:
            raise ValueError('Email and password are required')
        
        try:
            user = UserService.get_user_by_email(email)
            if not user or not bcrypt.check_password_hash(user.password, password):
                raise ValueError('Invalid email or password')
            
            access_token = create_access_token(identity=user.id)
            return {'access_token': access_token}
        except ValueError as e:
            raise
        except Exception as e:
            abort(500, description='Internal server error')

    @staticmethod
    def logout():
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            abort(400, 'Authorization header is required')
        
        try:
            access_token = auth_header.split(' ')[1]
        except IndexError:
            abort(400, 'Invalid Authorization header format')
        
        try:
            decoded_token = decode_token(access_token)
            jti = decoded_token['jti']
            BlocklistController.revoke_token(jti)
            return '', 204
        except ValueError as e:
            raise
        except Exception as e:
            abort(500, description='Internal server error')

    @staticmethod
    @jwt_required()
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
    @jwt_required()
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
    @jwt_required()
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