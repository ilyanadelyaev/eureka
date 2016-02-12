import flask

import eureka.logic.user

from eureka.view.api.register import blueprint


@blueprint.route('/user/', methods=['POST', 'GET'])
def users():
    """
    * POST (Create)
        201 = Created
        409 = Conflict
        404 = Error
    * GET (Read)
        200 = OK
    """
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
    elif flask.request.method == 'GET':  # read
        objs = flask.g.controller.user.all()
        resp_data = {
            'objects': objs,
            'count': len(objs),
        }
        return flask.jsonify(resp_data), 200
    else:
        flask.abort(405)  # invalid method


@blueprint.route('/user/<int:pk>/', methods=['GET', 'PUT', 'DELETE'])
def user(pk):
    """
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
    if flask.request.method == 'GET':  # read
        obj = flask.g.controller.user.one(pk)
        if not obj:
            flask.abort(404)
        return flask.jsonify(obj), 200
    else:
        flask.abort(405)  # invalid method
