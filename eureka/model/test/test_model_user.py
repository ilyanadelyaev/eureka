import pytest

import sqlalchemy.exc

import eureka.model.user


class TestUserModel:
    def test__user(
            self, session_scope,
            user_name, user_email
    ):
        """
        Create
        """
        _user_id = None
        with session_scope() as session:
            user = eureka.model.user.User(
                name=user_name,
                email=user_email,
            )
            session.add(user)
            session.flush()
            _user_id = user.id
        with session_scope() as session:
            obj = session.query(
                eureka.model.user.User
            ).filter_by(id=_user_id).first()
            assert obj.name == user_name
            assert obj.email == user_email

    def test__user__email_non_unique(
        self, session_scope,
        user_name, user_email
    ):
        """
        Non-unique email
        """
        with session_scope() as session:
            user_1 = eureka.model.user.User(
                name=user_name,
                email=user_email,
            )
            session.add(user_1)
            session.flush()
            #
            user_2 = eureka.model.user.User(
                name=user_name,
                email=user_email,
            )
            session.add(user_2)
            # IntegrityError: column email is not unique
            with pytest.raises(sqlalchemy.exc.IntegrityError):
                session.flush()
            session.rollback()  # clean session after exception
