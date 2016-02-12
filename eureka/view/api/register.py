import flask


blueprint = flask.Blueprint('api', __name__, url_prefix='/api')


def register_views(flask_app):
    """
    views register magic
    """
    flask_app.register_blueprint(blueprint)
