import logging

import flask

import eureka.logic.user
import eureka.logic.exc

from eureka.view.api.base import blueprint


logger = logging.getLogger('view')


@blueprint.route('/user/', methods=['POST'])
def create_user():
    """
    * POST (Create)
        201 = Created
        409 = Conflict
        404 = Error
    """
    resp_data = None
    resp_code = None
    #
    if flask.request.json:
        try:
            name = flask.request.json.get('name', '')
            email = flask.request.json.get('email', '')
            user_id = flask.g.controller.user.create(name, email)
            resp_data, resp_code = {'id': user_id}, 200
        except eureka.logic.user.AlreadyExists as ex:
            logger.exception(ex)
            resp_data, resp_code = {'error': ex.message}, 409
        except (
                eureka.logic.exc.InvalidArgument,
                eureka.logic.user.UserError,
        ) as ex:
            logger.exception(ex)
            resp_data, resp_code = {'error': ex.message}, 404
        except Exception as ex:  # pylint: disable=W0703
            logger.exception(ex)
            resp_data, resp_code = {'error': 'Internal error'}, 404
    else:
        resp_data, resp_code = {'error': 'Invalid data'}, 404
    #
    return flask.jsonify(resp_data), resp_code


@blueprint.route('/user/<int:pk>/', methods=['GET'])
def read_user(pk):
    """
    * GET (Read)
        200 = OK
        404 = Not found
    """
    resp_data = None
    resp_code = None
    #
    try:
        obj = flask.g.controller.user.one(pk)
        resp_data, resp_code = obj, 200
    except eureka.logic.user.NotExists as ex:
        logger.exception(ex)
        resp_data, resp_code = {'error': ex.message}, 404
    except Exception as ex:  # pylint: disable=W0703
        logger.exception(ex)
        resp_data, resp_code = {'error': 'Internal error'}, 404
    #
    return flask.jsonify(resp_data), resp_code


@blueprint.route('/user/', methods=['GET'])
def read_users():
    """
    * GET (Read)
        200 = OK
        404 = Not found
    """
    resp_data = None
    resp_code = None
    #
    objs = flask.g.controller.user.all()
    resp_data = {
        'objects': objs,
        'count': len(objs),
    }
    resp_code = 200
    #
    return flask.jsonify(resp_data), resp_code


@blueprint.route('/user/<int:pk>/', methods=['PUT'])
def update_user(pk):
    """
    * PUT (Update)
        200 = OK
        204 = No content
        404 = Not found
    """
    resp_data = None
    resp_code = None
    #
    if not flask.request.json:
        return flask.jsonify({'error': 'Invalid data'}), 204
    try:
        name = flask.request.json.get('name', '')
        email = flask.request.json.get('email', '')
        flask.g.controller.user.update(pk, name, email)
        resp_data, resp_code = {'result': 'OK'}, 200
    except eureka.logic.user.NotExists as ex:
        logger.exception(ex)
        resp_data, resp_code = {'error': ex.message}, 404
    except (
            eureka.logic.exc.InvalidArgument,
            eureka.logic.user.UserError,
    )as ex:
        logger.exception(ex)
        resp_data, resp_code = {'error': ex.message}, 204
    except Exception as ex:  # pylint: disable=W0703
        logger.exception(ex)
        resp_data, resp_code = {'error': 'Internal error'}, 404
    #
    return flask.jsonify(resp_data), resp_code


@blueprint.route('/user/<int:pk>/', methods=['DELETE'])
def delete_user(pk):
    """
    * DELETE
        200 = OK
        404 = Not found
    """
    resp_data = None
    resp_code = None
    #
    try:
        flask.g.controller.user.delete(pk)
        resp_data, resp_code = {'result': 'OK'}, 200
    except eureka.logic.user.NotExists as ex:
        logger.exception(ex)
        resp_data, resp_code = {'error': ex.message}, 404
    except Exception as ex:  # pylint: disable=W0703
        logger.exception(ex)
        resp_data, resp_code = {'error': 'Internal error'}, 404
    #
    return flask.jsonify(resp_data), resp_code
