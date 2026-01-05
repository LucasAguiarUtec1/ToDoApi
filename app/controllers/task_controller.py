from flask import abort, jsonify, request
from app.services.task_service import TaskService
from app.services.user_service import UserService
from flask_jwt_extended import jwt_required, get_jwt_identity

class TaskController:
    @staticmethod
    @jwt_required()
    def create_task():
        data = request.get_json(silent=True)
        if not data:
            abort(400, 'request must be JSON')
        
        name = data.get('name')
        user_id = get_jwt_identity()
        expires_in = data.get('expires_in')

        if name is None or user_id is None or expires_in is None:
            abort(400, 'All fields are required')

        try:
            user = UserService.get_user_by_id(user_id)
            if not user:
                raise ValueError('User not found')
            return TaskService.crate_task(name=name, user_id=user_id, expires_in=expires_in)
        except ValueError as e:
            raise
        except Exception as e:
            abort(500, description='Internal server error')
    
    @staticmethod
    @jwt_required()
    def complete_task(id):
        if not id:
            raise ValueError('Bad request')
        
        try:
            return TaskService.complete_task(id)
        except ValueError as e:
            raise
        except Exception as e:
            abort(500, description='Internal server error')

    @staticmethod
    @jwt_required()
    def delete_task(id):
        if not id:
            raise ValueError('Bad request')

        try:
            TaskService.delete_task(id)
            return '', 204
        except ValueError as e:
            raise
        except Exception as e:
            abort(500, description='Internal server error')

    @staticmethod
    @jwt_required()
    def update_task(id):
        if not id:
            raise ValueError('Bad request')

        data = request.get_json(silent=True)
        if not data:
            abort(400, 'request must be JSON')
        
        name = data.get('name')
        expires_in = data.get('expires_in')

        if name is None and expires_in is None:
            abort(400, 'At least one field is required to update')
        
        try:
            return TaskService.update_task(id, name=name, expires_in=expires_in)
        except ValueError as e:
            raise
        except Exception as e:
            abort(500, description='Internal server error')

    @staticmethod
    @jwt_required()
    def get_paginated_user_tasks(user_id, page, per_page):
        try:
            return TaskService.get_paginated_user_tasks(user_id, page, per_page)
        except Exception as e:
            abort(500, description='Internal server error')
    