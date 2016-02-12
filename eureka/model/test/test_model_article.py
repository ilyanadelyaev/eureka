import pytest

import sqlalchemy.orm.exc

import eureka.model.article
import eureka.model.user


class TestArticle:
    def test__article(self, session_scope, article_text):
        """
        Create
        """
        _id = None
        with session_scope() as session:
            article = eureka.model.article.Article(
                text=article_text,
            )
            session.add(article)
            session.flush()
            _id = article.id
        with session_scope() as session:
            obj = session.query(
                eureka.model.article.Article
            ).filter_by(id=_id).first()
            assert obj.text == article_text

    def test__article_star(
            self, session_scope,
            user_email, article_text
    ):
        """
        Create
        """
        _arcitle_id = None
        _user_id = None
        with session_scope() as session:
            user = eureka.model.user.User(
                email=user_email,
            )
            article = eureka.model.article.Article(
                text=article_text,
            )
            session.add_all((user, article))
            session.flush()
            _user_id = user.id
            _arcitle_id = article.id
            #
            star = eureka.model.article.Star(
                arcitle_id=article.id,
                user_id=user.id,
            )
            session.add(star)
            session.flush()
        with session_scope() as session:
            obj = session.query(
                eureka.model.article.Star
            ).filter_by(arcitle_id=_arcitle_id).first()
            assert _user_id == obj.user_id

    def test__article_star__non_unique(
            self, session_scope,
            user_email, article_text
    ):
        """
        Start (arcitle_id, user_id) unique
        """
        with session_scope() as session:
            user = eureka.model.user.User(
                email=user_email,
            )
            article = eureka.model.article.Article(
                text=article_text,
            )
            session.add_all((user, article))
            session.flush()
            #
            star_1 = eureka.model.article.Star(
                arcitle_id=article.id,
                user_id=user.id,
            )
            session.add(star_1)
            session.flush()
            #
            star_2 = eureka.model.article.Star(
                arcitle_id=article.id,
                user_id=user.id,
            )
            session.add(star_2)
            # FlushError: New instance N with identity key (..)
            # conflicts with persistent instance M
            with pytest.raises(sqlalchemy.orm.exc.FlushError):
                session.flush()
            session.rollback()  # clean session after exception
