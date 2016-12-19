# -*- coding: utf-8 -*-
__author__ = 'David Pinheiro'

from flask import jsonify, request, url_for
from flask_babel import gettext as _
from flask.ext.restful import reqparse, Resource
from flask_restful.inputs import regex
from sqlalchemy.orm.exc import NoResultFound

from flask_template.logger.log import create_logger, log
from flask_template.models import get_session, User
from flask_template.util import CustomArgument, create_base_response

logger = create_logger(__name__)


class UserAPI(Resource):

    def __init__(self):
        self.reqparse = reqparse.RequestParser(bundle_errors=True,
                                               argument_class=CustomArgument)
        
        self.reqparse.add_argument(
                'uuid', type=str, required=False, location='args')

        if request.method == 'POST':
            self.reqparse.add_argument(
                'name', type=str, required=True, location='json',
                help=_('field %(field)s is required', field='name'))

            self.reqparse.add_argument(
                'email', required=True,
                type=regex(r'(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)'), 
                location='json', 
                help=_('field %(field)s is required', field='email'))

            self.reqparse.add_argument(
                'username', type=str, required=True, location='json',
                help=_('field %(field)s is required', field='username'))

            self.reqparse.add_argument(
                'password', type=str, required=True, location='json',
                help=_('field %(field)s is required', field='password'))

        elif request.method == 'GET':
            self.reqparse.add_argument(
                'fields', type=str, action='append', required=False,
                help=_('limit_help_msg'))

            self.reqparse.add_argument(
                'limit', type=int, required=False, location='args',
                help=_('limit_help_msg'))

            self.reqparse.add_argument(
                'offset', type=int, required=False,
                location='args', help=_('offset_help_msg'))


        super(UserAPI, self).__init__()


    def post(self):
        args = self.reqparse.parse_args()
        response = create_base_response()

        del args['uuid']
        user = User(**args)

        session = get_session()
        session.add(user)
        session.commit()

        response['user'] = user.as_dict()
        response['message'] = _('User successfully registered')
        log(logger, response['uuid'], response)
        
        resource_url = url_for('users', user_id=user.id)
        return response, 201, {'Location': resource_url}


    def get(self, user_id=None):
        args = self.reqparse.parse_args()
        desired_fields = args['fields']
        response = create_base_response()
        session = get_session()

        try:
            if user_id is not None:
                users = [
                    session.query(User).filter(User.id == user_id).one()]
            else:
                limit = args['limit']
                offset = args['offset']

                query = session.query(User)
                query = query.limit(limit) if limit else query
                query = query.offset(offset) if offset else query
                users = query.all()

                response['total_count'] = len(users)
            
            response['users'] = [user.as_dict(desired_fields=desired_fields) for user in users]
            status_code = 200

        except NoResultFound:
            response['message'] = _('User not found')
            status_code = 404
        
        log(logger, response['uuid'], response, status_code=status_code)
        return response, status_code


    def delete(self, user_id=None):
        response = create_base_response()
        session = get_session()

        try:
            user = session.query(User).filter(User.id == user_id).one()

            session.delete(user)
            session.commit()

            response['message'] = _('User successfully removed')
            status_code = 200
        except NoResultFound:
            response['message'] = _('User not found')
            status_code = 404

        log(logger, response['uuid'], response, status_code=status_code)
        return response, status_code


class StatusAPI(Resource):

    def get(self):
        """endpoint for monitoring services"""

        response = create_base_response()
        response['message'] = 'running'
        log(logger, response['uuid'], response, level='info')
        return jsonify(response)


def not_found(error):
    """handler for not_found error"""

    response = create_base_response()
    response['message'] = _('Endpoint not found')
    log(logger, response['uuid'], response, level='error')
    return jsonify(response), 404
