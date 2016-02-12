import uuid

import pytest

import configure

import eureka.application


@pytest.fixture(scope='session')
def config():
    """
    Test config
    """
    return configure.Configuration.from_file(
        './dev/test/config.yaml').configure()


@pytest.fixture(scope='session')
# pylint: disable=W0621
def application(config):
    """
    Application
    """
    return eureka.application.Application(config)


@pytest.fixture(scope='session')
# pylint: disable=W0621
def session_scope(application):
    return application.db_engine.session_scope


@pytest.fixture(scope='session')
# pylint: disable=W0621
def controller(application):
    return application.controller


########################################


@pytest.fixture
def article_text():
    return str(uuid.uuid4()) * 20


@pytest.fixture
def user_name():
    return str(uuid.uuid4())


@pytest.fixture
def user_email():
    return '{}@example.com'.format(uuid.uuid4())
