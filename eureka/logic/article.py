import logging

import sqlalchemy.exc
import sqlalchemy.orm.exc

import eureka.tools.retry

import eureka.logic.exc
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

    @staticmethod
    def __validate_text(text):
        """
        validate name length bounds: (0..
        raises on error
        """
        if not text:
            raise eureka.logic.exc.InvalidArgument('text', text)

    # rewrite it to specific errors
    # TimeoutError
    @eureka.tools.retry.retry((sqlalchemy.exc.SQLAlchemyError,), logger=logger)
    def create(self, auth_id, text):
        """
        Create article
        return obj_id
        raises on error
        """
        #
        self.__validate_text(text)
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
                auth_user, article = session.query(
                    eureka.model.auth.AuthUser,
                    eureka.model.article.Article,
                ).join(eureka.model.article.Article).filter(
                    (
                        eureka.model.auth.AuthUser.id ==
                        eureka.model.article.Article.auth_id
                    ) & (
                        eureka.model.article.Article.id == pk
                    )
                ).order_by(
                    eureka.model.article.Article.id.desc()
                ).one()
                result = {'auth_email': auth_user.email}
                result.update(article.to_dict())
                return result
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
            query = session.query(
                eureka.model.auth.AuthUser,
                eureka.model.article.Article,
            ).join(eureka.model.article.Article).filter(
                eureka.model.auth.AuthUser.id ==
                eureka.model.article.Article.auth_id
            ).order_by(
                eureka.model.article.Article.id.desc()
            )
            result = []
            for auth_user, article in query.all():
                dct = {'auth_email': auth_user.email}
                dct.update(article.to_dict())
                result.append(dct)
            return result
