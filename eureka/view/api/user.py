import flask

from eureka.view.api.register import blueprint


@blueprint.route('/user/', methods=['GET'])
def users():
    """
    Users list
    """
    resp_data = {}
    resp_code = 200

    objs = flask.g.controller.user.all()
    resp_data['objects'] = objs
    resp_data['count'] = len(objs)

    return flask.jsonify(resp_data), resp_code
