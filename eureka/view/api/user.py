import flask

import eureka.logic.user

from eureka.view.api.base import blueprint


@blueprint.route('/user/', methods=['POST', 'GET'])
@blueprint.route('/user/<int:pk>/', methods=['GET', 'PUT', 'DELETE'])
# pylint: disable=R0912
def user(pk=None):
    """
    * POST (Create)
        201 = Created
        409 = Conflict
        404 = Error
    * GET (Read)
        200 = OK
        404 = Not found
    * PUT (Update)
        200 = OK
        204 = No content
        404 = Not found
    * DELETE
        200 = OK
        404 = Not found
    """
    resp_data = None
    resp_code = None
    #
    if flask.request.method == 'POST':  # create
        try:
            result = flask.g.controller.user.create(flask.request.json)
        except eureka.logic.user.AlreadyExists as ex:
            return flask.jsonify({'error': ex.message}), 409
        except eureka.logic.user.UserError as ex:
            return flask.jsonify({'error': ex.message}), 404
        resp_data = {
            'obj_id': result,
        }
        return flask.jsonify(resp_data), 200
    #
    elif flask.request.method == 'GET':  # read
        if pk is None:
            objs = flask.g.controller.user.all()
            resp_data = {
                'objects': objs,
                'count': len(objs),
            }
            resp_code = 200
        else:
            try:
                obj = flask.g.controller.user.one(pk)
                resp_data, resp_code = obj, 200
            except eureka.logic.user.NotExists as ex:
                resp_data, resp_code = {'error': ex.message}, 404
    #
    elif flask.request.method == 'PUT':  # update
        try:
            flask.g.controller.user.update(pk, flask.request.json)
            resp_data, resp_code = {'result': 'OK'}, 200
        except eureka.logic.user.NotExists as ex:
            resp_data, resp_code = {'error': ex.message}, 404
        except eureka.logic.user.UserError as ex:
            resp_data, resp_code = {'error': ex.message}, 204
    #
    elif flask.request.method == 'DELETE':
        try:
            flask.g.controller.user.delete(pk)
            resp_data, resp_code = {'result': 'OK'}, 200
        except eureka.logic.user.NotExists as ex:
            resp_data, resp_code = {'error': ex.message}, 404
    else:
        flask.abort(405)  # invalid method
    #
    return flask.jsonify(resp_data), resp_code
