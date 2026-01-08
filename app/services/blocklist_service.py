from app import db
from app.models.blocklist import Blocklist

class BlocklistService:
    @staticmethod
    def is_token_revoked(jti):
        blocklist_entry = Blocklist.query.filter_by(jti=jti).first()
        return True if blocklist_entry else False
    
    @staticmethod
    def revoke_token(jti):
        blocklist_entry = Blocklist(jti=jti)
        db.session.add(blocklist_entry)
        db.session.commit()
        return ''