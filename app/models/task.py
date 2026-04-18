from app import db
from datetime import datetime

class Task(db.Model):
    __tablename__ = 'tasks'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    completed = db.Column(db.Boolean, default=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    expires_in = db.Column(db.DateTime, nullable=False)
    expired = db.Column(db.Boolean, default=False, nullable=False)

    user_id = db.Column(
        db.Integer, 
        db.ForeignKey('users.id', ondelete='CASCADE'),
        nullable=False
    )

    user = db.relationship(
        'User',
        back_populates='tasks'
    )

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'completed': self.completed,
            'created_at': self.created_at.isoformat(),
            'expires_in': self.expires_in.isoformat(),
            'expired': self.expired,
            'user_id': self.user_id
        }