from flask import Flask, request, abort
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from flask_restx import Api
from app.config import Config
from flask_jwt_extended import JWTManager
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import redis as redislib

db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()
limiter = Limiter(key_func=get_remote_address, default_limits=['200 per minute'])

@jwt.token_in_blocklist_loader
def check_if_token_revoked(jwt_header, jwt_payload):
    from app.controllers.blocklist_controller import BlocklistController
    jti = jwt_payload.get('jti')
    if jti is None:
        return False
    return BlocklistController.is_token_revoked(jti)


@jwt.revoked_token_loader
def revoked_token_callback(jwt_header, jwt_payload):
    return {"error": "The token has been revoked"}, 401


@jwt.invalid_token_loader
def invalid_token_callback(error):
    return {"error": f"Invalid token: {error}"}, 422


@jwt.unauthorized_loader
def missing_token_callback(error):
    return {"error": "Request does not contain an access token"}, 401


@jwt.expired_token_loader
def expired_token_callback(jwt_header, jwt_payload):
    return {"error": "The token has expired"}, 401

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    jwt.init_app(app)

    db.init_app(app)
    migrate.init_app(app, db)
    CORS(app)

    app.config.setdefault('RATELIMIT_STORAGE_URL', 'redis://localhost:6379/0')
    limiter.init_app(app)

    app.redis_client = redislib.from_url(app.config['RATELIMIT_STORAGE_URL'])

    @app.before_request
    def check_blocklist_and_progressive_ban():
        ip = request.remote_addr or get_remote_address()
        r = app.redis_client

        if r.get(f"ban:{ip}"):
            abort(429, description="Too many requests. You are temporarily banned.")
        
        key = f"req:{ip}"
        n = r.incr(key)
        if n == 1:
            r.expire(key, 60)
        
        if n > 300:
            r.setex(f"ban:{ip}", timedelta(minutes=30), 1)
            abort(429, description="Temporarily banned due to high request.")

    authorizations = {
        'Bearer Auth': {
            'type': 'apiKey',
            'in': 'header',
            'name': 'Authorization',
            'description': "Introduzca el token JWT con el prefijo 'Bearer <token>'"
        }
    }

    api = Api(
        app,
        version='1.0',
        title='Api Todo',
        desccription='Api con Flask-RESTX y Swagger UI',
        doc='/docs',
        prefix='/api',
        authorizations=authorizations,
    )

    @api.errorhandler(ValueError)
    def handle_value_error(error):
        return {"error": str(error)}, 404

    from app.routes import user_routes, task_routes
    api.add_namespace(user_routes.ns, path='/users')
    api.add_namespace(task_routes.ns, path='/tasks')

    return app