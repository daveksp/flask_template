# -*- coding: utf-8 -*-
import os

from flask import Flask, request
from flask_babel import Babel
from flask_cors import CORS
from flask.ext.restful import Api
from newrelic import agent

from config.general_config import Config
from flask_template.models import init_engine, close_connection
from flask_template.views import UserAPI, StatusAPI, not_found

app = Flask(__name__)
api = Api(app)
babel = Babel(app)

def configure_app():
    try:
        environment = os.environ['FLASKTEMPLATE_ENV']
    except KeyError:
        environment = 'Testing'
        os.environ['FLASKTEMPLATE_ENV'] = environment

    config = Config.factory(environment)
    app.config.from_object(config)


def start_database_engine():
    init_engine(
    	app.config['DB_URI'], 
    	app.config['DB_MIGRATE'],
    	echo=app.config['SQL_ALCHEMY_ECHO'])
    

def create_endpoints():
    api.add_resource(
        UserAPI, 
        '/flask_template/api/v1/users', 
        endpoint='user')

    api.add_resource(
        UserAPI, 
        '/flask_template/api/v1/users/<int:user_id>',
        endpoint='users')

    api.add_resource(
        StatusAPI, 
        '/flask_template/api/v1/status',
        endpoint='status')

    app.error_handler_spec[None][404] = not_found


def setup_cors():
    CORS(
        app, 
        resources={r"/flask_template/api/*": {
            "origins": str(app.config['CORS'])}}, 
        allow_headers='Content-Type',
        supports_credentials=True)


def start_newrelic():
    environment = os.environ['FLASKTEMPLATE_ENV']
    if environment != 'Testing':
        agent.initialize(app.config['NEW_RELIC_INI_PATH'], environment.lower())


@app.teardown_appcontext
def teardown_connection(exception):
    close_connection()


@babel.localeselector
def get_locale():
    return request.accept_languages.best_match(app.config['LANGUAGES'].keys())


configure_app()
start_database_engine()
create_endpoints()
setup_cors()
start_newrelic()