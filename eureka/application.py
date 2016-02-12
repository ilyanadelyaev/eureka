import logging

import gevent.wsgi
import flask

import eureka.tools.log

import eureka.database.engine
import eureka.logic.controller
import eureka.view.registry


class Application(object):
    """
    Flask application
    Use run() to start serving requests
    """

    def __init__(self, config):
        """
        - Initialize logic controller
        - Initialize flask app and register views
        - Set @app.before_request and @app.after_request
          send controller to each request via flask.g
        - Setup logging
        """
        self.config = config

        # database engine
        self.db_engine = eureka.database.engine.DBEngine(config)

        # logic controller
        self.controller = eureka.logic.controller.Controller(self.db_engine)

        # flask app
        self.flask_app = flask.Flask('eureka')
        eureka.view.registry.register_views(self.flask_app)
        eureka.view.registry.register_flask_before_request(self)

        # logging
        eureka.tools.log.setup_logging(config, self.flask_app)
        self.logger = logging.getLogger('eureka')

        #
        self.logger.info('Initialized')
        self.logger.info('Config: "%s"', str(config))

    def run(self):
        """
        Run flask application
        """
        self.logger.info('Started')
        server = gevent.wsgi.WSGIServer(
            (
                self.config.system.wsgi.host,
                self.config.system.wsgi.port,
            ),
            self.flask_app,
        )
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            pass
        self.logger.info('Terminated')
