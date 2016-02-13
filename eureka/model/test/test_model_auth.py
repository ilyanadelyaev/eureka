import pytest

import sqlalchemy.exc

import eureka.model.auth
import eureka.tools.crypto


class TestAuthUser:
    """
    Auth user model
    """

    def test__auth_user(
            self, session_scope,
            email, auth_token
    ):
        """
        Create auth user
        """
        with session_scope() as session:
            auth_user = eureka.model.auth.AuthUser(
                email=email,
                auth_token=auth_token,
            )
            session.add(auth_user)
            session.flush()
            auth_user = session.query(
                eureka.model.auth.AuthUser
            ).filter_by(id=auth_user.id).one()
            assert auth_user.id is not None
            assert auth_user.email == email
            assert auth_user.auth_token == auth_token

    def test__auth_user__email_not_unique(
            self, session_scope,
            email
    ):
        """
        Create auth user - email not unique
        """
        with pytest.raises(sqlalchemy.exc.IntegrityError):
            with session_scope() as session:
                auth_user_1 = eureka.model.auth.AuthUser(email=email)
                auth_user_2 = eureka.model.auth.AuthUser(email=email)
                session.add_all([auth_user_1, auth_user_2])


class TestAuthPassword:
    """
    Auth password model
    """

    def test__user_password(
            self, session_scope,
            email, password
    ):
        """
        Create auth password
        """
        hashed, salt = eureka.tools.crypto.Crypto.hash_passphrase(password)
        #
        with session_scope() as session:
            auth_user = eureka.model.auth.AuthUser(email=email)
            session.add(auth_user)
            session.flush()
            auth_password = eureka.model.auth.AuthPassword(
                auth_id=auth_user.id, hashed=hashed, salt=salt)
            session.add(auth_password)
            session.flush()
            #
            auth_password = session.query(eureka.model.auth.AuthPassword).join(
                eureka.model.auth.AuthUser).filter(
                    eureka.model.auth.AuthUser.email == email).one()
            assert auth_password.hashed == hashed
            assert auth_password.salt == salt

    def test__user_password__auth_id_not_unique(
            self, session_scope,
            email, password
    ):
        """
        Create auth password - auth_id not unique
        """
        hashed, salt = eureka.tools.crypto.Crypto.hash_passphrase(password)
        #
        with pytest.raises(sqlalchemy.exc.IntegrityError):
            with session_scope() as session:
                auth_user = eureka.model.auth.AuthUser(email=email)
                session.add(auth_user)
                session.flush()
                auth_password_1 = eureka.model.auth.AuthPassword(
                    auth_id=auth_user.id, hashed=hashed, salt=salt)
                auth_password_2 = eureka.model.auth.AuthPassword(
                    auth_id=auth_user.id, hashed=hashed, salt=salt)
                session.add_all([auth_password_1, auth_password_2])

    def test__simple__rollback(self, session_scope, email, password):
        """
        test rollback for auth records
        """
        hashed, salt = eureka.tools.crypto.Crypto.hash_passphrase(password)
        #
        with session_scope() as session:
            auth_user = eureka.model.auth.AuthUser(email=email)
            session.add(auth_user)
            session.flush()
            auth_password = eureka.model.auth.AuthPassword(
                auth_id=auth_user.id, hashed=hashed, salt=salt)
            session.add(auth_password)
            session.flush()
            session.rollback()
            assert not session.query(sqlalchemy.sql.exists().where(
                eureka.model.auth.AuthUser.email == email)).scalar()
            assert not session.query(sqlalchemy.sql.exists().where(
                eureka.model.auth.AuthPassword.hashed == hashed)).scalar()
