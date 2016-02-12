import pytest


@pytest.fixture(scope='session')
def session_scope(application):
    return application.db_engine.session_scope
