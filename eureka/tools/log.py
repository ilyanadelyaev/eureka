import os

import logging
import logging.handlers


def setup_logging(config, flask_app):
    """
    Setup components logs
    """

    # ensure dirs
    if config.system.logger.handler_type == 'file':
        if not os.path.exists(config.system.logger.path):
            os.makedirs(config.system.logger.path)

    # setup handler
    handler = __handler(config)

    # sqlalchemy
    __setup_logger(
        'sqlalchemy',
        config.system.logger.level,
        handler,
    )

    # flask
    flask_app.logger.addHandler(handler)
    flask_app.logger.setLevel(config.system.logger.level)

    # view
    __setup_logger(
        'view',
        config.system.logger.level,
        handler,
    )

    # eureka
    __setup_logger(
        'eureka',
        config.system.logger.level,
        handler,
    )


def __handler(config):
    """
    Rotating file handler for logger redirection
    Rotate every midnight
    or
    Stream handler
    """
    formatter = logging.Formatter(
        '[%(asctime)s] %(levelname)s [%(name)s] %(message)s'
    )
    #
    if config.system.logger.handler_type == 'file':
        handler = logging.handlers.TimedRotatingFileHandler(
            filename=os.path.join(
                config.system.logger.path,
                config.system.logger.filename,
            ),
            when='midnight',
            interval=1,
        )
    else:
        handler = logging.StreamHandler()  # pylint: disable=R0204
    #
    handler.setLevel(config.system.logger.level)
    handler.setFormatter(formatter)
    return handler


def __setup_logger(log_name, logging_level, handler):
    """
    Write specified messages for log class :log_name:
    to handler :handler: with :logging_level:
    """
    log = logging.getLogger(log_name)
    log.setLevel(logging_level)
    log.addHandler(handler)
