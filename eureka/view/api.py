import flask


blueprint = flask.Blueprint('api', 'eureka', url_prefix='/api')


def register_views(flask_app):
    """
    views register magic
    """
    flask_app.register_blueprint(blueprint)


@blueprint.route('/test/', methods=['GET'])
def test():
    """
    test
    """
    resp_data = {}
    resp_code = 200

    resp_data['result'] = flask.g.controller.test()

    return flask.jsonify(resp_data), resp_code
