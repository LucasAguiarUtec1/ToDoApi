from flask_restx import Namespace, Resource, fields, reqparse
from app.controllers.task_controller import TaskController

ns = Namespace('tasks', description='Operaciones disponibles para las tareas')

task_model = ns.model('Task', {
    'id': fields.Integer(readonly=True, description='Id de la tarea'),
    'name': fields.String(required=True, description='Nombre de la tarea'),
    'completed': fields.Boolean(required=True, description='Estado en el que se encuentra la tarea. True=completada / False=no completada'),
    'created_at': fields.DateTime(description='Fecha de creacion'),
    'expires_in': fields.DateTime(required=True, description='Fecha limite/expiracion de la tarea'),
    'user_id': fields.Integer(readonly=True, description='Id del usuario al cual le pertenece la tarea')
})

task_input = ns.model('Task_input', {
    'name': fields.String(required=True, description='Nombre de la tarea'),
    'expires_in': fields.DateTime(required=True, description='Fecha limite/expiracion de la tarea')
})

task_input_update = ns.model('Task_input_update', {
    'name': fields.String(required=False, description='Nombre de la tarea'),
    'expires_in': fields.DateTime(required=False, description='Fecha limite/expiracion de la tarea')
})

@ns.route('/')
class TaskList(Resource):
    @ns.doc('create_task', security='Bearer Auth')
    @ns.expect(task_input)
    @ns.marshal_with(task_model, 201)
    def post(self):
        '''Crear una nueva tarea'''
        return TaskController.create_task()
    
@ns.route('/<int:id>/complete')
@ns.param('id', 'El id de la tarea')
class TaskComplete(Resource):
    @ns.doc('complete_task', security='Bearer Auth')
    @ns.marshal_with(task_model)
    def put(self, id):
        '''Marcar una tarea como completada'''
        return TaskController.complete_task(id)

@ns.route('/<int:id>')
@ns.param('id', 'El id de la tarea')
class TaskResource(Resource):
    @ns.doc('delete_task', security='Bearer Auth')
    def delete(self, id):
        '''Eliminar una tarea'''
        return TaskController.delete_task(id)
    
    @ns.doc('update_task', security='Bearer Auth')
    @ns.expect(task_input_update)
    @ns.marshal_with(task_model)
    def put(self, id):
        '''Actualizar una tarea'''
        return TaskController.update_task(id)
    
@ns.route('/user/<int:user_id>')
@ns.param('user_id', 'El id del usuario')
class UserTasks(Resource):
    @ns.doc('get_user_tasks', security='Bearer Auth')
    @ns.param('page', 'Numero de pagina', type=int, default=1)
    @ns.param('per_page', 'Tareas por pagina', type=int, default=10)
    def get(self, user_id):
        '''Obtener tareas paginadas de un usuario'''
        parser = reqparse.RequestParser()
        parser.add_argument('page', type=int, location='args', default=1)
        parser.add_argument('per_page', type=int, location='args', default=10)
        args = parser.parse_args()

        page = args.get('page', 1)
        per_page = args.get('per_page', 10)

        return TaskController.get_paginated_user_tasks(user_id, page, per_page)