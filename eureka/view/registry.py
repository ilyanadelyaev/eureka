import uuid
import logging

import flask

from . import api
from . import web


logger = logging.getLogger('view')


def register_views(flask_app):
    """
    views register magic
    """
    for module in (api, web, ):
        flask_app.register_blueprint(module.blueprint)


def register_flask_callbacks(application):
    """
    Register here all specific methods per-request call
    """

    # callback functiion
    # pylint: disable=W0612
    @application.flask_app.before_request
    def before_request():
        """
        - Send controller to request
        - Set request_id
        - Log request data
        """
        # controller
        flask.g.controller = application.controller
        # request id
        flask.g.request_id = str(uuid.uuid4())
        # logging
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
    @application.flask_app.after_request
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
