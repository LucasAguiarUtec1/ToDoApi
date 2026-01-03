from app import db
from app.models.task import Task

class TaskService:
    @staticmethod
    def crate_task( name, user_id, expires_in):
        task = Task(name=name, completed=False, expires_in=expires_in, user_id=user_id)
        db.session.add(task)
        db.session.commit()
        return task.serialize()
    
    @staticmethod
    def complete_task(id):
        task = Task.query.get(id)
        if not task:
            raise ValueError("Task not found")
        
        task.completed = True
        db.session.commit()
        return task.serialize()
    
    @staticmethod
    def delete_task(id):
        task = Task.query.get(id)

        if not task:
            raise ValueError("Task not found")
        
        db.session.delete(task)
        db.session.commit()
        return
    
    @staticmethod
    def update_task(id, name, expires_in):
        task = Task.query.get(id)
        if not task:
            raise ValueError('Task not found')
        
        if task.completed:
            raise ValueError('Completed tasks cannot be updated')

        if name.strip():
            task.name = name
        
        if expires_in:
            task.expires_in = expires_in

        db.session.commit()
        return task.serialize()
    
    @staticmethod
    def get_paginated_user_tasks(user_id, page, per_page):
        paginated_tasks = Task.query.filter_by(user_id=user_id).paginate(page=page, per_page=per_page, error_out=False)
        return {
            'tasks': [task.serialize() for task in paginated_tasks.items],
            'total': paginated_tasks.total,
            'pages': paginated_tasks.pages,
            'current_page': paginated_tasks.page
        }