import flask


blueprint = flask.Blueprint('web', __name__, url_prefix='/')


@blueprint.route('/', methods=['GET'])
def index():
    return flask.render_template('index.html')
