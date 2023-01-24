from logging import getLogger
from pyramid.httpexceptions import (
    HTTPNotFound,
    HTTPBadRequest,
    HTTPConflict
)
from pyramid.view import view_config
from json import loads


class ExceptionViews:
    ''' Class to create and raise httpexceptions. '''
    def __init__(self, msg, request_body):
        self.msg = msg
        self.request_body = request_body
        self.view_name = 'ExceptionViews'
        self.log = getLogger(__name__)
        if self.request_body.body == b'':
            parameters = self.request_body.matchdict['username']
        else:
            parameters = loads(self.request_body.body)
        self.response = {
            'parameters': parameters,
            'method': self.request_body.method,
            'Url': self.request_body.url,
            'msg': str(self.msg)
        }

    @view_config(context=HTTPBadRequest, renderer='json')
    def badrequest_view(self):
        ''' Raise httpbadrequest. '''
        self.log.info('Raise a httpbadrequest (%s)', self.msg)
        return HTTPBadRequest(self.response)

    @view_config(context=HTTPConflict, renderer='json')
    def conflict_view(self):
        ''' Raise httpconflict. '''
        self.log.info('Raise a httpconflict (%s)', self.msg)
        return HTTPConflict(self.response)

    @view_config(context=HTTPNotFound, renderer='json')
    def notfound_view(self):
        ''' Raise httpnotfound. '''
        self.log.info('Raise a httpnotfound (%s)', self.msg)
        return HTTPNotFound(self.response)
