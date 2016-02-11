import uuid
import logging

import flask

from . import api


logger = logging.getLogger('view')


def register_views(flask_app):
    """
    views register magic
    """
    for module in (api, ):
        module.register_views(flask_app)


def register_flask_before_request(flask_app, controller):
    """
    Register here all specific methods per-request call
    """

    # callback functiion
    # pylint: disable=W0612
    @flask_app.before_request
    def before_request():
        """
        - Send controller to request
        - Set request_id
        - Log request data
        """
        flask.g.controller = controller
        #
        flask.g.request_id = str(uuid.uuid4())
        #
        request = flask.request
        message = '[{}] {} -> ({} {})'.format(
            flask.g.request_id,
            request.remote_addr,
            request.path, request.method,
        )
        if request.mimetype == 'application/json':
            message += ' {}'.format(request.data)
        logger.info(message)

    # callback functiion
    # pylint: disable=W0612
    @flask_app.after_request
    def after_request(resp):
        """
        - Log request data
        """
        message = '[{}] ({})'.format(
            flask.g.request_id,
            resp.status_code,
        )
        if resp.mimetype == 'application/json':
            message += ' {}'.format(resp.data.replace('\n', ''))
        logger.info(message)
        return resp
