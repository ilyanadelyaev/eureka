import pytest

import eureka.model.auth
import eureka.model.article
import eureka.logic.article


class TestArticleManager:
    @staticmethod
    def __create_auth(session_scope, email):
        """
        auth creation helper
        """
        _auth_id = None
        with session_scope() as session:
            # clear table
            eureka.model.auth.AuthUser.query.delete()
            #
            auth = eureka.model.auth.AuthUser(
                email=email,
            )
            session.add(auth)
            session.flush()
            _auth_id = auth.id
        return _auth_id

    @staticmethod
    def __create_article(session_scope, auth_id, text):
        """
        article creation helper
        """
        _article_id = None
        with session_scope() as session:
            # clear table
            eureka.model.article.Article.query.delete()
            #
            article = eureka.model.article.Article(
                auth_id=auth_id,
                text=text,
            )
            session.add(article)
            session.flush()
            _article_id = article.id
        return _article_id

    def test__create(
            self, controller,
            session_scope, email, article_text
    ):
        """
        Create article
        """
        auth_id = self.__create_auth(session_scope, email)
        #
        obj_id = controller.article.create(auth_id, article_text)
        #
        obj = controller.article.one(obj_id)
        assert obj['auth_id'] == auth_id
        assert obj['text'] == article_text

    def test__one(
            self, controller,
            session_scope, email, article_text
    ):
        """
        One article
        """
        auth_id = self.__create_auth(session_scope, email)
        _article_id = self.__create_article(
            session_scope, auth_id, article_text)
        #
        obj = controller.article.one(_article_id)
        #
        assert obj['auth_id'] == auth_id
        assert obj['text'] == article_text

    def test__one__not_exists(
            self, controller,
            session_scope, email,
    ):
        """
        One article - not exists
        """
        with pytest.raises(eureka.logic.article.NotExists) as ex_info:
            controller.article.one(0)
        assert ex_info.value.message == \
            'Article "0" is not exists'

    def test__all(
            self, controller,
            session_scope, email, article_text
    ):
        """
        All articles
        """
        auth_id = self.__create_auth(session_scope, email)
        self.__create_article(session_scope, auth_id, article_text)
        #
        objs = controller.article.all()
        #
        assert len(objs) == 1
        assert objs[0]['auth_id'] == auth_id
        assert objs[0]['text'] == article_text
