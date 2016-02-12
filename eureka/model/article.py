import sqlalchemy

import eureka.database.base


class Article(eureka.database.base.AuditBaseModel):
    """
    Articles
    """

    __tablename__ = 'articles'

    id = sqlalchemy.Column(
        sqlalchemy.Integer,
        primary_key=True,
    )

    text = sqlalchemy.Column(
        sqlalchemy.Text,
    )


class Star(eureka.database.base.AuditBaseModel):
    """
    Article stars
    """

    __tablename__ = 'article_stars'

    arcitle_id = sqlalchemy.Column(
        sqlalchemy.Integer,
        sqlalchemy.ForeignKey('articles.id'),
        primary_key=True,  # unique record
    )

    user_id = sqlalchemy.Column(
        sqlalchemy.Integer,
        sqlalchemy.ForeignKey('users.id'),
        primary_key=True,  # unique record
    )
