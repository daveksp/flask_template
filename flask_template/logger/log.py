__author__ = 'David Pinheiro'
"""
Created on 07/27/2016

Module responsible for provinding logging features.
"""

import os
import logging
from logging import StreamHandler
from logging.handlers import RotatingFileHandler
import inspect
from re import match

LOG_LOCATION = '/var/log/flask_template/'
LOG_NAME = 'flask_template.log'


formatter = logging.Formatter(
    '%(asctime)s - %(levelname)s - %(name)s.%(funcName)s - PID:%(process)d - TID:%(thread)d - %(message)s')


if not os.path.exists(LOG_LOCATION):
    os.makedirs(LOG_LOCATION)


def create_logger(class_name):
    """create logger based on class_name

    :param class_name: The class for attaching the logger.
    """

    logger = logging.getLogger('{0}'.format(class_name))
    has_stream_handler = False
    has_file_handler = False
    handlers = []

    handlers.append(StreamHandler())
    location = LOG_LOCATION + LOG_NAME
    handlers.append(RotatingFileHandler(location, 
                                        maxBytes=10000000,
                                        backupCount=10))

    for handler in handlers:
        handler.setLevel(logging.INFO)
        handler.setFormatter(formatter)
        logger.setLevel(logging.INFO)
        logger.addHandler(handler)

    return logger


def log(logger, uuid_value, response, level="info", params=None, status_code=None):
    """defines a standard to messages and log them

    :param logger logger: The sender logger object.
    :param uuid_value: The uuid value related to the incomming request.
    :param response: The response for the incomming request.
    :param level: The severity level to label the log message. 
    :param params: The parameters received with the request.
    :status_code: The status code for automatic detection of severity level.
    """

    error_status = match(r'^[4-5][0-9]{2}$', str(status_code))
    if error_status is not None:
        level = 'error'


    method = inspect.stack()[1][0].f_code.co_name
    msg = ('uuid={}, caller={}, calling_method={}, params={}, msg={}'
           .format(uuid_value, '', method, params, response))

    getattr(logger, level)(msg)
