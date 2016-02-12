import sqlalchemy

import eureka.database


class User(eureka.database.Base):
    """
    Users
    """

    __tablename__ = 'users'

    id = sqlalchemy.Column(
        sqlalchemy.Integer,
        primary_key=True,
    )
    name = sqlalchemy.Column(
        sqlalchemy.String(60),
    )
    email = sqlalchemy.Column(
        sqlalchemy.String(150),
        unique=True,
    )
