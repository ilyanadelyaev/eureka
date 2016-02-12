import sqlalchemy

import eureka.database.base


class User(eureka.database.base.BaseModel):
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
