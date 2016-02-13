import sqlalchemy

import eureka.database.base
import eureka.tools.crypto


class AuthUser(eureka.database.base.BaseModel):
    """
    :id: is system wide auth_id
    :email: must be unique
    :auth_token: user token
    """
    __tablename__ = 'auth_user'

    id = sqlalchemy.Column(
        sqlalchemy.Integer,
        primary_key=True,
    )
    email = sqlalchemy.Column(
        sqlalchemy.String(120),
        unique=True,
        index=True,
    )
    auth_token = sqlalchemy.Column(
        sqlalchemy.String(
            eureka.tools.crypto.Crypto.auth_token_length),
        index=True,  # to process future api reqiests with token
    )


class AuthPassword(eureka.database.base.BaseModel):
    """
    :hashed: and :salt: to securely store user password
    """
    __tablename__ = 'auth_password'

    auth_id = sqlalchemy.Column(
        sqlalchemy.Integer,
        sqlalchemy.ForeignKey('auth_user.id'),
        primary_key=True,  # one user - one password
    )
    hashed = sqlalchemy.Column(
        sqlalchemy.String(eureka.tools.crypto.Crypto.hashed_length)
    )
    salt = sqlalchemy.Column(
        sqlalchemy.String(eureka.tools.crypto.Crypto.salt_length)
    )
