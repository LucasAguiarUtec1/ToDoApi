from flask_restx import Namespace, Resource, fields
from app.controllers.user_controller import UserController
from app import limiter

ns = Namespace('users', description='Operaciones de usuarios')

user_model = ns.model('User', {
    'id': fields.Integer(readonly=True, description='ID del usuario'),
    'username': fields.String(required=True, description='Nombre del usuario'),
    'email': fields.String(required=True, description='Email del usuario'),
    'created_at': fields.DateTime(description='Fecha de creacion')
})

user_input = ns.model('UserInput', {
    'username': fields.String(required=True, description='Nombre de usuario'),
    'email': fields.String(required=True, description='Email del usuario'),
    'password': fields.String(required=True, description='Contraseña del usuario')
})

user_input_put = ns.model('UserInputUpdate', {
    'username': fields.String(required=False, description='Nombre del usuario'),
    'email': fields.String(required=False, description='Email del usuario')
})

login_input = ns.model('LoginInput', {
    'email': fields.String(required=True, description='Email del usuario'),
    'password': fields.String(required=True, description='Contraseña del usuario')
})

@ns.route('/')
class UserList(Resource):
    @ns.doc('list_users', security='Bearer Auth')
    @ns.marshal_list_with(user_model)
    def get(self):
        '''Listar todos los usuarios'''
        return UserController.get_users()
    
    @ns.doc('create_user')
    @ns.expect(user_input)
    @ns.marshal_with(user_model, code=201)
    @limiter.limit("10 per minute")
    def post(self):
        '''Crear nuevo usuario'''
        return UserController.create_user()
    
@ns.route("/<int:id>")
class UserResource(Resource):
    @ns.doc('delete_user', security='Bearer Auth')
    @ns.response(204, 'Usuario eliminado')
    def delete(self, id):
        '''Eliminar un usuario por id'''
        return UserController.delete_user(id)
    
    @ns.doc('update_user')
    @ns.expect(user_input_put)
    def put(self, id):
        '''Actualizar un usuario'''
        return UserController.update_user(id)

@ns.route('/login')
class UserLogin(Resource):
    @ns.doc('login_user')
    @ns.expect(login_input)
    @limiter.limit("5 per minute")
    def post(self):
        '''Login de usuario'''
        return UserController.login()
    
@ns.route('/logout')
class UserLogout(Resource):
    @ns.doc('logout_user', security='Bearer Auth')
    def post(self):
        '''Logout de usuario'''
        return UserController.logout()