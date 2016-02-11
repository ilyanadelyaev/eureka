import os

import logging
import logging.handlers


def setup_logging(config, flask_app):
    """
    Setup components logs
    """

    # ensure dirs
    if not os.path.exists(config.system.logger.path):
        os.makedirs(config.system.logger.path)

    # sql log: sqlalchemy
    __setup_logger(
        'sqlalchemy',
        os.path.join(
            config.system.logger.path,
            config.system.logger.sql
        ),
        config.system.logger.level,
    )

    # flask log
    flask_app.logger.addHandler(__logging_file_handler(
        os.path.join(
            config.system.logger.path,
            config.system.logger.system
        ),
        config.system.logger.level,
    ))
    flask_app.logger.setLevel(config.system.logger.level)

    # view log: view
    __setup_logger(
        'view',
        os.path.join(
            config.system.logger.path,
            config.system.logger.view
        ),
        config.system.logger.level,
    )

    # app log: eureka
    __setup_logger(
        'eureka',
        os.path.join(
            config.system.logger.path,
            config.system.logger.app
        ),
        config.system.logger.level,
    )


def __logging_file_handler(filename, logging_level):
    """
    Get time rotating file handler for logger redirection
    Rotate every midnight
    """
    file_handler = logging.handlers.TimedRotatingFileHandler(
        filename=filename,
        when='midnight',
        interval=1,
    )
    file_handler.setLevel(logging_level)
    formatter = logging.Formatter(
        '[%(asctime)s] %(levelname)s [%(name)s] %(message)s'
    )
    file_handler.setFormatter(formatter)
    return file_handler


def __setup_logger(log_name, filename, logging_level):
    """
    Write specified messages for log class :log_name:
    to file :filename: with :logging_level:
    """
    file_handler = __logging_file_handler(filename, logging_level)
    log = logging.getLogger(log_name)
    log.setLevel(logging_level)
    log.addHandler(file_handler)
