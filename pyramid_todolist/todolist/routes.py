''' Routes fot pyrimad api. '''

def includeme(config):
    ''' Routes for pyramid api views. '''
    config.add_route('info', 'api/v1')
    config.add_route('users', 'api/v1/accounts')
    config.add_route('user', 'api/v1/accounts/{username}')
    config.add_route('tasks', 'api/v1/accounts/{username}/tasks')
    config.add_route('task', 'api/v1/accounts/{username}/task')
