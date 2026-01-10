from app.services.blocklist_service import BlocklistService

class BlocklistController:
    @staticmethod
    def is_token_revoked(jti):
        return BlocklistService.is_token_revoked(jti)
    
    @staticmethod
    def revoke_token(jti):
        return BlocklistService.revoke_token(jti)