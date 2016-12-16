# coding: utf-8
__author__ = 'david'

import json
import unittest

from flask_babel import lazy_gettext as _

import flask_template
from flask_template import app, util
from flask_template.config.general_config import Config         
from flask_template.models import get_session, init_engine, User


class manageTestCase(unittest.TestCase):  


    def setUp(self):
        self.app = app.test_client()

    # tests for util module
    def test_create_base_response(self):
        with app.test_request_context('/test'):
            response = util.create_base_response()

            assert 'message' in response
            assert response['uuid'] is not None
            assert len(response) == 2
        

    # tests for models module
    def test_user_as_dict_default_fields(self):
        user = User(
            name='David Pinheiro', email='daveksp@gmail.com', 
            username='daveksp', password='pass123')
        
        with app.test_request_context('/test'):
            user_json = user.as_dict()
        
            assert user_json['username'] == 'daveksp' 
            assert len(user_json) == 4


    def test_user_as_dict_desired_fields(self):
        user = User(
            name='David Pinheiro', email='daveksp@gmail.com', 
            username='daveksp', password='pass123')
        
        with app.test_request_context('/test'):
            user_json = user.as_dict(desired_fields=['name'])
        
            assert user_json['name'] == 'David Pinheiro'    
            assert len(user_json) == 1


    def test_user_to_string(self):
        user = User(
            name='David Pinheiro', email='daveksp@gmail.com', 
            username='daveksp', password='pass123', id=None)
        
        user_as_string = "User(id=None, name='David Pinheiro', email='daveksp@gmail.com', username='daveksp', password='pass123')"
        assert str(user) == user_as_string

        user_from_str = eval(user_as_string)
        assert user_from_str.name == 'David Pinheiro'

        del user.__dict__['_sa_instance_state']
        del user_from_str.__dict__['_sa_instance_state']

        assert user.__dict__ == user_from_str.__dict__



    # tests for views module
    def test_not_found_handler(self):
        with flask_template.app.test_request_context('/test'):
            rv = self.app.get('/flask_template/api/v2/pipocas')
            tags = json.loads(rv.data)
            
            assert tags['message'] == _('Endpoint not found')
            assert rv._status_code == 404


    def test_status_endpoint(self):
        rv = self.app.get('/flask_template/api/v1/status')
        tags = json.loads(rv.data)

        assert tags['message'] == 'running'
        assert rv._status_code == 200


    # tests for config module
    def test_config(self):
        self.assertRaises(TypeError, Config.factory, 'Pipocas')
        

if __name__ == '__main__':
	unittest.main()