import logging

import sqlalchemy.exc
import sqlalchemy.orm.exc

import eureka.tools.retry

import eureka.logic.base
import eureka.model.article


logger = logging.getLogger('eureka')


class ArticleError(eureka.logic.exc.LogicError):
    pass


class NotExists(ArticleError):
    def __init__(self, pk):
        super(NotExists, self).__init__(
            'Article "{}" is not exists'.format(pk))


class ArticleManager(eureka.logic.base.ManagerBase):
    """
    Article manager
    """

    # rewrite it to specific errors
    # TimeoutError
    @eureka.tools.retry.retry((sqlalchemy.exc.SQLAlchemyError,), logger=logger)
    def create(self, auth_id, text):
        """
        Create article
        return obj_id
        """
        #
        _article_id = None
        with self.db_engine.session_scope() as session:
            article = eureka.model.article.Article(
                auth_id=auth_id,
                text=text,
            )
            session.add(article)
            session.flush()
            _article_id = article.id
        return _article_id

    # rewrite it to specific errors
    # TimeoutError
    @eureka.tools.retry.retry((sqlalchemy.exc.SQLAlchemyError,), logger=logger)
    def one(self, pk):
        """
        Get one article
        return {obj} or None
        raises on error
        """
        try:
            with self.db_engine.session_scope() as session:
                obj = session.query(
                    eureka.model.article.Article
                ).filter_by(id=pk).one()
                return obj.to_dict()
        except sqlalchemy.orm.exc.NoResultFound:
            raise NotExists(pk)

    # rewrite it to specific errors
    # TimeoutError
    @eureka.tools.retry.retry((sqlalchemy.exc.SQLAlchemyError,), logger=logger)
    def all(self):
        """
        Get all articles
        return [{obj}, ...]
        """
        with self.db_engine.session_scope() as session:
            return [o.to_dict() for o in session.query(
                eureka.model.article.Article).all()]
