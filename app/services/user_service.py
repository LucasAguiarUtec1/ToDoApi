from app import db
from app.models.user import User

class UserService:
    @staticmethod
    def create_user(username, email, password):
        if User.query.filter_by(username=username).first() or User.query.filter_by(email=email).first():
            raise ValueError("The email or username is already associated with an existing account.")
        user = User(username=username, email=email, password=password)
        db.session.add(user)
        db.session.commit()
        return user.serialize()
    
    @staticmethod
    def get_all_users():
        return User.query.all()
    
    @staticmethod
    def get_user_by_id(id):
        user = User.query.get(id)
        return user.serialize() if user else None

    @staticmethod
    def delete_user(id):
        user = User.query.get(id)

        if not user:
            raise ValueError("User not found")
        
        db.session.delete(user)
        db.session.commit()
        return
    
    @staticmethod
    def update_user(id, username, email):
        user = User.query.get(id)
        if not user:
            raise ValueError('User not found')
        
        if username.strip():
            user.username = username
        
        if email.strip():
            user.email = email

        db.session.commit()
        return
    