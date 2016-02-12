import pytest
import flask_webtest


@pytest.fixture(scope='session')
def web_app(application):
    return flask_webtest.TestApp(application.flask_app)
