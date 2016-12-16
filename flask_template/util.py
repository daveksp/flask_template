__author__ = 'David Pinheiro'

import uuid
import six

from flask import request
from flask_babel import gettext as _
from flask.ext.restful.reqparse import Argument

from flask_template.logger.log import create_logger, log

logger = create_logger(__name__)

def create_base_response():
    """Creates a base response to be used as standard

    Creates a base response to be used in the entire application.
    This way, it'll be easy to use another log analysis tool such 
    as the ELK Suite (Elastic search, Logstash and Kibana)
    """

    uuid_value = request.args.get('uuid')

    if uuid_value is None:
        uuid_value = str(uuid.uuid4())

    response = dict(uuid=uuid_value, message='')
    if request.method == 'POST':
        params = request.get_data()
    else:
        params = request.args

    log(logger, response['uuid'], 'starting request', params=params)

    return response


class CustomArgument(Argument):
    """Custom Argument class to be used with RequestParser"""

    def handle_validation_error(self, error, bundle_errors):
        """Called when an error is raised while parsing. Aborts the request
        with a 400 status and an error message
        :param error: the error that was raised
        :param bundle_errors: do not abort when first error occurs, return a
            dict with the name of the argument and the error message to be
            bundled
        """
        
        error_str = six.text_type(error)
        error_msg = self.help.format(error_msg=error_str) if self.help else error_str
        msg = {self.name: error_msg}

        if bundle_errors:
            return error, msg
        flask_restful.abort(400, message=msg)
