import logging

import flask

import eureka.logic.exc
import eureka.logic.auth
import eureka.logic.article

from eureka.view.api.base import blueprint


logger = logging.getLogger('view')


@blueprint.route('/article/', methods=['POST'])
def create_article():
    """
    * POST (Create)
        201 = Created
        404 = Error
    """
    resp_data = None
    resp_code = None
    #
    if flask.request.json:
        try:
            auth_token = flask.request.json.get('auth_token', '')
            text = flask.request.json.get('text', '')
            #
            auth_id = flask.g.controller.auth.get_id_by_token(auth_token)
            article_id = flask.g.controller.article.create(auth_id, text)
            #
            resp_data, resp_code = {'id': article_id}, 201
        except (
                eureka.logic.exc.InvalidArgument,
                eureka.logic.article.ArticleError,
                eureka.logic.auth.NotExists,
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


@blueprint.route('/article/<int:pk>/', methods=['GET'])
def read_article(pk):
    """
    * GET (Read)
        200 = OK
        404 = Not found
    """
    resp_data = None
    resp_code = None
    #
    try:
        obj = flask.g.controller.article.one(pk)
        resp_data, resp_code = obj, 200
    except eureka.logic.article.NotExists as ex:
        logger.exception(ex)
        resp_data, resp_code = {'error': ex.message}, 404
    except Exception as ex:  # pylint: disable=W0703
        logger.exception(ex)
        resp_data, resp_code = {'error': 'Internal error'}, 404
    #
    return flask.jsonify(resp_data), resp_code


@blueprint.route('/article/', methods=['GET'])
def read_articles():
    """
    * GET (Read)
        200 = OK
        404 = Not found
    """
    resp_data = None
    resp_code = None
    #
    objs = flask.g.controller.article.all()
    resp_data = {
        'objects': objs,
        'count': len(objs),
    }
    resp_code = 200
    #
    return flask.jsonify(resp_data), resp_code
