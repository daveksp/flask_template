__author__ = 'david'
"""
Created on 07/27/2016

@author David Pinheiro

@summary:
    - Config
        - ProductionConfig
        - DevelopmentConfig
        - TestingConfig

Module responsible for provinding configuration details according to
especific Enviroment Types such as Production, Testing and Development.
"""
import os

class Config(object):
    DB_MIGRATE = True
    DB_URI = ''
    SQL_ALCHEMY_ECHO = False

    SECRET_KEY = '\xae\xdc\xa0\xb6\xbf\x843\xe5EELd\x99\x07Tt\x92\x16\xa5\xddj\xf0@\xe8'
    NEW_RELIC_INI_PATH = 'resources/newrelic.ini'

    DEBUG = True
    TESTING = True

    LANGUAGES = {
        'en': 'English',
        'pt': 'Portuguese'
    }

    @staticmethod
    def factory(type):
        """Factory method for handling Config's subclasses creation

        Classes are wrapped inside method for preventing them to be
        directly instanciated. Re-assign desired variables that
        should assume different values inside each subclass.

        @param type: subclass name

        @raise TypeError: When provinding a non existent subclass name
        """

        type = type + 'Config'

        class ProductionConfig(Config):
            DB_URI = 'sqlite:////opt/apps/walmart_backend/walmart.db'
            DEBUG = False
            SQL_ALCHEMY_ECHO = False


        class DevelopmentConfig(Config):
            DB_URI = 'sqlite:////Users/davidpinheiro/Documents/projetos/flask_template/flasktemplate.db'

        class TestingConfig(Config):
            DB_URI = ''.join(['sqlite:///', os.getcwd(), '/flasktemplate_test.db'])
            SQL_ALCHEMY_ECHO = False
            LOG_LOCATION = 'log/'

        subclasses = Config.__subclasses__()
        types = [subclass.__name__ for subclass in subclasses]

        if type not in types:
            raise TypeError('Invalid Enviroment Type. Possible values: ' + str(types))
        else:
            return eval(type + '()')
