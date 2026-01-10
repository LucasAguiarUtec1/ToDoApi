from app import db
from datetime import datetime

class Blocklist(db.Model):
    __tablename__ = 'blocklists'

    id = db.Column(db.Integer, primary_key=True)
    jti = db.Column(db.String(36), nullable=False, unique=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def serialize(self):
        return {
            'id': self.id,
            'jti': self.jti,
            'created_at': self.created_at.isoformat()
        }