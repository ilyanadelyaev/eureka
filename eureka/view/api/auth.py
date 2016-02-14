import logging

import flask

from eureka.view.api.base import blueprint

import eureka.logic.auth
import eureka.logic.exc


logger = logging.getLogger('view')


@blueprint.route('/auth/signup', methods=['POST'])
def signup():
    """
    Signup user
    """
    resp_data = None
    resp_code = None
    #
    if flask.request.method == 'POST':
        if flask.request.json:
            try:
                email = flask.request.json.get('email', '')
                password = flask.request.json.get('password', '')
                flask.g.controller.auth.register(email, password)
                resp_data, resp_code = {'result': 'OK'}, 201
            except eureka.logic.auth.AlreadyExists as ex:
                logger.exception(ex)
                resp_data, resp_code = {'error': ex.message}, 409
            except eureka.logic.exc.InvalidArgument as ex:
                logger.exception(ex)
                resp_data, resp_code = {'error': ex.message}, 404
            except Exception as ex:  # pylint: disable=W0703
                logger.exception(ex)
                resp_data, resp_code = {'error': 'Internal error'}, 404
        else:
            resp_data, resp_code = {'error': 'Invalid data'}, 404
    else:
        flask.abort(405)  # invalid method
    #
    return flask.jsonify(resp_data), resp_code


@blueprint.route('/auth/signin', methods=['POST'])
def signin():
    """
    Signin user
    """
    resp_data = None
    resp_code = None
    cookies = []
    #
    if flask.request.method == 'POST':
        if flask.request.json:
            try:
                email = flask.request.json.get('email', '')
                password = flask.request.json.get('password', '')
                # pylint: disable=W0612
                auth_token = flask.g.controller.auth.get_auth_token(
                    email, password)
                # set cookie with auth_token
                cookies.append(('auth_email', email or ''))
                cookies.append(('auth_token', auth_token or ''))
                #
                resp_data, resp_code = {'result': 'OK'}, 200
            except (
                    eureka.logic.exc.InvalidArgument,
                    eureka.logic.auth.NotExists,
                    eureka.logic.auth.AuthError,
            ) as ex:
                logger.exception(ex)
                resp_data, resp_code = {'error': ex.message}, 404
            except Exception as ex:  # pylint: disable=W0703
                logger.exception(ex)
                resp_data, resp_code = {'error': 'Internal error'}, 404
        else:
            resp_data, resp_code = {'error': 'Invalid data'}, 404
    else:
        flask.abort(405)  # invalid method
    #
    response = flask.jsonify(resp_data)
    for cookie in cookies:
        response.set_cookie(*cookie)
    return response, resp_code
