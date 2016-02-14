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

    auth_id = sqlalchemy.Column(
        sqlalchemy.Integer,
        sqlalchemy.ForeignKey('auth_user.id'),
    )

    text = sqlalchemy.Column(
        sqlalchemy.Text,
    )

    def to_dict(self):
        """
        fixme
        """
        return {
            'id': self.id,
            'auth_id': self.auth_id,
            'text': self.text,
        }


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

    auth_id = sqlalchemy.Column(
        sqlalchemy.Integer,
        sqlalchemy.ForeignKey('auth_user.id'),
        primary_key=True,  # unique record
    )
