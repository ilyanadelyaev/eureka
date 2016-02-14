import pytest

import sqlalchemy.orm.exc

import eureka.model.article
import eureka.model.auth


class TestArticle:
    def test__article(
            self, session_scope,
            email, article_text
    ):
        """
        Create
        """
        _auth_id = None
        _article_id = None
        with session_scope() as session:
            auth = eureka.model.auth.AuthUser(
                email=email,
            )
            session.add(auth)
            session.flush()
            _auth_id = auth.id
            #
            article = eureka.model.article.Article(
                auth_id=auth.id,
                text=article_text,
            )
            session.add(article)
            session.flush()
            _article_id = article.id
        with session_scope() as session:
            obj = session.query(
                eureka.model.article.Article
            ).filter_by(id=_article_id).first()
            assert obj.auth_id == _auth_id
            assert obj.text == article_text

    def test__article_star(
            self, session_scope,
            email, article_text
    ):
        """
        Create
        """
        _arcitle_id = None
        _auth_id = None
        with session_scope() as session:
            auth = eureka.model.auth.AuthUser(
                email=email,
            )
            article = eureka.model.article.Article(
                text=article_text,
            )
            session.add_all((auth, article))
            session.flush()
            _auth_id = auth.id
            _arcitle_id = article.id
            #
            star = eureka.model.article.Star(
                arcitle_id=article.id,
                auth_id=auth.id,
            )
            session.add(star)
            session.flush()
        with session_scope() as session:
            obj = session.query(
                eureka.model.article.Star
            ).filter_by(arcitle_id=_arcitle_id).first()
            assert _auth_id == obj.auth_id

    def test__article_star__non_unique(
            self, session_scope,
            email, article_text
    ):
        """
        Start (arcitle_id, auth_id) unique
        """
        with session_scope() as session:
            auth = eureka.model.auth.AuthUser(
                email=email,
            )
            article = eureka.model.article.Article(
                text=article_text,
            )
            session.add_all((auth, article))
            session.flush()
            #
            star_1 = eureka.model.article.Star(
                arcitle_id=article.id,
                auth_id=auth.id,
            )
            session.add(star_1)
            session.flush()
            #
            star_2 = eureka.model.article.Star(
                arcitle_id=article.id,
                auth_id=auth.id,
            )
            session.add(star_2)
            # FlushError: New instance N with identity key (..)
            # conflicts with persistent instance M
            with pytest.raises(sqlalchemy.orm.exc.FlushError):
                session.flush()
            session.rollback()  # clean session after exception
