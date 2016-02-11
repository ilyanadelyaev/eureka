import argparse
import logging

import gevent.wsgi
import flask
import configure

import eureka.tools.log

import eureka.logic.controller
import eureka.view.registry


def parse_args():
    """
    Add command-line arguments here
    """
    # command line arguments parser
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--config',
        required=True,
        help='path to application config',
    )
    return parser.parse_args()


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

        # logic controller
        self.controller = eureka.logic.controller.Controller()

        # flask app
        self.flask_app = flask.Flask('eureka')
        eureka.view.registry.register_views(self.flask_app)
        eureka.view.registry.register_flask_before_request(
            self.flask_app, self.controller)

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


if __name__ == '__main__':
    args = parse_args()

    # load system config and start application
    Application(
        configure.Configuration.from_file(
            args.config
        ).configure()
    ).run()
