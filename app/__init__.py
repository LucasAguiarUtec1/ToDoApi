from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from flask_restx import Api
from app.config import Config

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    CORS(app)

    api = Api(
        app,
        version='1.0',
        title='Api Todo',
        desccription='Api con Flask-RESTX y Swagger UI',
        doc='/docs',
        prefix='/api'
    )

    @api.errorhandler(ValueError)
    def handle_value_error(error):
        return {"error": str(error)}, 404

    from app.routes import user_routes, task_routes
    api.add_namespace(user_routes.ns, path='/users')
    api.add_namespace(task_routes.ns, path='/tasks')

    return app