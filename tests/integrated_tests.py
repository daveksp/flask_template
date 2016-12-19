# coding: utf-8
__author__ = 'david'

import json
import os
from StringIO import StringIO
import sys
import time
import unittest

from flask_babel import lazy_gettext as _
from mock import patch, MagicMock

import flask_template
from flask_template import app, util
from flask_template.config.general_config import Config         
from flask_template.models import get_session, init_engine, User


class manageTestCase(unittest.TestCase):  
    
    initialized = False

    @classmethod
    def setUpClass(cls):
        manageTestCase.init_db()

    
    @classmethod
    def tearDownClass(cls):
        manageTestCase.remove_entries()


    def setUp(self):
        self.app = app.test_client()
        self.inserted_users = []
        
                
    def tearDown(self):
        session = get_session()

        for user_id in self.inserted_users:
            session.query(User).filter_by(id=user_id).delete()
            session.commit()
        
    # Tests for User View
    def test_add_user(self):
        user_json = json.dumps(dict(
            name='New User', email='new_user@test.com',
            username='new_user', password='pass123'
        ))
        rv = self.app.post('/flask_template/api/v1/users', 
                           data=user_json,
                           headers={'Content-Type': 'application/json'})
        
        user = json.loads(rv.data)   
        assert user['message'] == _('User successfully registered')
        self.inserted_users.append(user['user']['id'])

    
    def test_add_user_missing_values(self):
        rv = self.app.post('/flask_template/api/v1/users', data=dict())
        
        user = json.loads(rv.data)   
        
        assert user['message']['username'] == _('field %(field)s is required', field='username') 
        assert user['message']['password'] == _('field %(field)s is required', field='password') 
        assert user['message']['email'] == _('field %(field)s is required', field='email') 
        assert user['message']['name'] == _('field %(field)s is required', field='name')

    
    def test_add_user_wrong_email_pattern(self):
        rv = self.app.post('/flask_template/api/v1/users', data=dict(
            name='New User', email='new_user@test',
            username='new_user', password='pass123'
        ))
        
        user = json.loads(rv.data)   
        
        assert user['message']['email'] == _('field %(field)s is required', field='email') 


    def test_list_user(self):
        rv = self.app.get('/flask_template/api/v1/users')
        user = json.loads(rv.data)
        assert user['total_count'] == 3


    def test_list_user_limit(self):
        rv = self.app.get('/flask_template/api/v1/users?limit=1')
        user = json.loads(rv.data)
        assert user['total_count'] == 1


    def test_list_user_offset(self):
        rv = self.app.get('/flask_template/api/v1/users?offset=1')
        user = json.loads(rv.data)
        assert user['total_count'] == 2
        assert user['users'][0]['id'] == 2


    def test_list_user_field_filtering(self):
        rv = self.app.get('/flask_template/api/v1/users?fields=id&fields=username')
        user = json.loads(rv.data)
        assert user['total_count'] == 3
        assert len(user['users'][0]) == 2
        assert user['users'][0]['id'] == 1
        assert user['users'][0]['username'] == 'test_user'


    # special_features = limit, offset and field filtering
    def test_list_user_special_features(self):
        rv = self.app.get('/flask_template/api/v1/users?limit=1&offset=1&fields=id&fields=email')
        user = json.loads(rv.data)
        assert user['total_count'] == 1
        assert len(user['users'][0]) == 2
        assert user['users'][0]['id'] == 2
        assert user['users'][0]['email'] == 'userretest@test.com'


    def test_get_product_by_id(self):
        rv = self.app.get('/flask_template/api/v1/users/1')
        user = json.loads(rv.data)   

        assert user['users'][0]['name'] == 'Test User'     


    def test_get_user_wrong_id(self):
        rv = self.app.get('/flask_template/api/v1/users/99999')
        product = json.loads(rv.data)   
        
        assert product['message'] == _('User not found')


    def test_delete_user_wrong_id(self):
        rv = self.app.delete('/flask_template/api/v1/users/99999')
        response = json.loads(rv.data)
        assert response['message'] == _('User not found')


    def test_delete_user(self):
        user_json = json.dumps(dict(
            name='test remove', email='remove@test.com',
            username='user_remove', password='pass123',
        ))
        rv = self.app.post('/flask_template/api/v1/users', 
                           data=user_json,
                           headers={'Content-Type': 'application/json'})
        
        user = json.loads(rv.data)
        user_id = user['user']['id']
        rv = self.app.delete('/flask_template/api/v1/users/' + str(user_id))
        response = json.loads(rv.data)

        assert response['message'] == _('User successfully removed')


    # Util methods   
    @staticmethod
    def init_db():   
        config = Config.factory('Testing') 
        init_engine(config.DB_URI, config.DB_MIGRATE ,echo=config.SQL_ALCHEMY_ECHO)
            
        session = get_session()

        user_a = User(id=1,
            name='Test User', email='user@test.com', 
            username='test_user', password='pass123')

        user_b = User(id=2,
            name='ReTest User', email='userretest@test.com', 
            username='retest_user', password='pass123')

        user_c = User(id=3,
            name='Final Test User', email='finaluserretest@test.com', 
            username='final_test_user', password='pass123')

        session.add(user_a)
        session.add(user_b)
        session.add(user_c)
        
        session.commit()


    @staticmethod
    def remove_entries():
        session = get_session()
        
        session.query(User).delete()
        session.commit()

if __name__ == '__main__':
	unittest.main()