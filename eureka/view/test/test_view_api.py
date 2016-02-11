import json

import pytest
import flask.ext.webtest

import eureka.application


@pytest.fixture(scope='session')
def web_app(config):
    application = eureka.application.Application(config)
    return flask.ext.webtest.TestApp(application.flask_app)


class TestAPI:
    def test__test(self, web_app):
        resp = web_app.get(
            '/api/test/'
        )
        assert resp.status_code == 200
