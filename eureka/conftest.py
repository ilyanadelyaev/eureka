import pytest

import configure


@pytest.fixture(scope='session')
def config():
    """
    Test config
    """
    return configure.Configuration.from_file(
        './dev/test/config.yaml').configure()
