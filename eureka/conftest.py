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
