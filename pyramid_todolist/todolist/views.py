from datetime import datetime
import json

import hydra

from logging import getLogger
from pyramid.view import (
    view_config,
    view_defaults
)
from pyramid.httpexceptions import (
    HTTPNotFound,
    HTTPBadRequest,
    HTTPConflict
)

from todolist.models import (
    Task,
    User
)

@hydra.InfoView(config_path='conf', config_name='config')
@view_defaults(route_name='info', request_method='GET', renderer='json')
class InfoView(cfg):
    def __init__(self, request):
        self.request = request
        self.view_name = 'InfoView'
        self.log = getLogger(__name__)
        print(cfg)

    @view_config(request_method='GET')
    def info_view(self):
        ''' Info view. '''
        self.log.info('Get all infos from pyramid server')
        return {
            'info': 'GET /api/v1',
            'create user': 'POST /api/v1/accounts',
            'list user': 'GET /api/v1/accounts',
            'get user details': 'GET /api/v1/accounts/<username>',
            'update user details': 'PUT /api/v1/accounts/<username>',
            'delete user details': 'DELETE /api/v1/accounts/<username>',
            'users tasks': 'GET /api/v1/accounts/<username>/tasks',
            'create task': 'POST /api/v1/accounts/<username>/tasks',
            'task details': 'GET /api/v1/accounts/<username>/tasks/<id>',
            'update task': 'PUT /api/v1/accounts/<username>/tasks/<id>',
            'delete task': 'DELETE /api/v1/accounts/<username>/tasks/<id>',
        }


@view_defaults(route_name='users', request_method=('GET', 'POST'), renderer='json')
class ClassView:
    def __init__(self, request):
        self.request = request
        self.view_name = 'ClassView'
        self.log = getLogger(__name__)

    @view_config(request_method='POST')
    def create_user_view(self):
        ''' Add user view. '''
        parameters = json.loads(self.request.body)
        self.log.info('Create user in sql-database with parameters: %s', parameters)
        if not all(parameter in parameters for parameter in ("username", "email", "password")):
            raise HTTPBadRequest('parameter missing you need: username, email, password')
        user = self.request.dbsession.query(User).filter_by(
               username=self.request.json['username']).first()
        if not user:
            new_user = User(**self.request.json)
            self.request.dbsession.add(new_user)
            return {'Success': 'New user created'}
        raise HTTPConflict('user already exsist!')

    @view_config(request_method='GET', renderer='json')
    def user_info_view(self):
        ''' Info user view. '''
        self.log.info('Get info from all user.')
        user_info = self.request.dbsession.query(User)
        result = []
        for user in user_info:
            info_response = {
                'username': user.username,
                'email': user.email,
                'password': user.password,
                'creation_date': str(user.date_joined)
            }
            result.append(info_response)
        return result



@view_defaults(route_name='user', request_method=('GET', 'POST', 'DELETE'), renderer='json')
class EditUserClass:
    def __init__(self, request):
        self.request = request
        self.view_name = 'ViewClass'
        self.log = getLogger(__name__)
        self.username = self.request.matchdict['username']
        self.user = self.request.dbsession.query(User).filter_by(username=self.username).first()
        if self.user is None:
            raise HTTPNotFound('User does not existing!')

    @view_config(request_method='GET')
    def query_view(self):
        ''' Query user view. '''
        self.log.info('Get info from user: %s', self.username)
        info_response = {
            'username': self.user.username,
            'email': self.user.email,
            'password': self.user.password,
            'creation_date': str(self.user.date_joined)
        }
        return info_response

    @view_config(request_method='DELETE')
    def delete_view(self):
        ''' Delete user view. '''
        self.log.info('Delete user: %s', self.username)
        self.request.dbsession.delete(self.user)
        return {'msg': 'User is deleted'}

    @view_config(request_method='PUT')
    def edit_view(self):
        ''' Edit user view. '''
        parameter = json.loads(self.request.body)
        self.log.info('Edit (%s) for user: %s', parameter, self.username)
        if 'password' in parameter:
            answer = self.request.dbsession.query(User).filter_by(username=self.username).update(
                    {User.password: parameter['password']}
            )
            return {'msg':'password is changed'}
        else:
            answer = self.request.dbsession.query(User).filter_by(username=self.username).update(
                    {User.email: parameter['email']}
            )
            return {'msg':'email is changed'}


@view_defaults(route_name='tasks', request_method=('GET', 'POST'), renderer='json')
class TaskView:
    def __init__(self, request):
        self.request = request
        self.view_name = 'TaskView'
        self.log = getLogger(__name__)
        self.username = self.request.matchdict['username']
        self.user = self.request.dbsession.query(User).filter_by(username=self.username).first()
        if self.user is None:
            raise HTTPNotFound('User does not existing!')

    @view_config(request_method='POST')
    def create_task_view(self):
        ''' Create task for user view. '''
        self.log.info('Create task for %s', self.username)
        parameter = json.loads(self.request.body)
        date = datetime.strptime(parameter['due_date'], '%d/%m/%Y').date()
        task = Task(
            name = parameter['name'],
            note = parameter['note'],
            due_date = date,
            user_id = self.user.id
        )
        self.request.dbsession.add(task)
        return {'Success': 'Task is created!'}

    @view_config(request_method='GET')
    def info_task(self):
        ''' Get task from user. '''
        task = self.request.dbsession.query(Task).filter_by(user_id=self.user.id)
        for user_task in task:
            task_info = {
                'name': user_task.name,
                'note': user_task.note,
                'creation_date': str(self.user.date_joined),
                'completed': False,
                'due_date': str(user_task.due_date),
                'id': self.user.id
            }
        return task_info


@view_defaults(route_name='task', request_method=('GET', 'PUT', 'DELETE'))
class EditTaskView:
    def __init__(self, request):
        self.request = request
        self.view_name = 'EditTaskView'
        self.log = getLogger(__name__)
        self.username = self.request.matchdict['username']
        self.user = self.request.dbsession.query(User).filter_by(username=self.username).first()
        if self.user == None:
            raise HTTPNotFound('User does not exist!')

    @view_config(request_method='GET', renderer='json')
    def info_user_task(self):
        ''' Get task from user. '''
        self.log.info('Get task for %s', self.username)
        task_id = self.request.matchdict['task_id']
        task = self.request.dbsession.query(Task).filter_by(id=task_id).first()
        if task == None:
            raise HTTPNotFound('Task for user does not exist!')
        task = self.request.dbsession.query(Task).filter_by(id=task_id)
        for user_task in task:
            task_info = {
                'name': user_task.name,
                'note': user_task.note,
                'creation_date': str(self.user.date_joined),
                'completed': False,
                'due_date': str(user_task.due_date),
                'id': self.user.id
            }
        return task_info

    @view_config(request_method='PUT', renderer='json')
    def update_task(self):
        ''' Update task for user. '''
        self.log.info('Update task for user: %s', self.username)
        task_id = self.request.matchdict['task_id']
        task = self.request.dbsession.query(Task).filter_by(user_id=task_id).first()
        if task == None:
            raise HTTPNotFound('Task for user does not exist!')

        parameters = json.loads(self.request.body)
        if any(parameter_check in parameters.keys() for parameter_check in ('id', 'creation_date')):
            raise HTTPBadRequest('id and creation_date cannot be changed!')

        check_parameters = ('name', 'due_date', 'note', 'completed')
        for para in parameters.keys():
            if para not in check_parameters:
                raise HTTPBadRequest('Only name, due_date, note and completed can be changed!')

        task = self.request.dbsession.query(Task).filter_by(user_id=task_id)
        for query_task in task:
            if 'name' in parameters.keys():
                new_name = parameters['name']
            else:
                new_name = query_task.name
            if 'note' in parameters.keys():
                new_note = parameters['note']
            else:
                new_note = query_task.note
            if 'due_date' in parameters.keys():
                new_date = datetime.strptime(parameters['due_date'], '%d.%m.%Y').date()
            else:
                new_date = query_task.due_date
            if 'completed' in parameters.keys():
                if parameters['completed'] == 'True':
                    completed = True
            else:
                completed = query_task.completed

            self.request.dbsession.query(Task).filter_by(id=query_task.id).update(
                {Task.name: new_name, Task.note: new_note,
                 Task.due_date: new_date, Task.completed: completed}
            )
        self.log.info('Task for user has been renewed')
        return {'success':'task is edit!'}

    @view_config(request_method='DELETE', renderer='json')
    def delete_task(self):
        ''' Delete task from user. '''
        self.log.info('Delete task from user: %s', self.username)
        task_id = self.request.matchdict['task_id']
        task = self.request.dbsession.query(Task).filter_by(id=task_id).first()
        if task == None:
             raise HTTPNotFound('Task for user does not exist!')
        self.request.dbsession.delete(task)
        return {'succes': 'User tasks have been deleted!'}
