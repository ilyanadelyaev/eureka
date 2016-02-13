import pytest

import eureka.tools.crypto
import eureka.model.auth
import eureka.logic.auth
import eureka.logic.exc


@pytest.fixture
def manager(db_engine):
    return eureka.logic.auth.AuthManager(db_engine)


class TestAuthManager:
    """
    Test auth manager
    """

    def test__update_auth_token(self):
        """
        Update auth token for user
        """
        auth_user = eureka.model.auth.AuthUser(
            email='email',
            auth_token=eureka.logic.auth.AuthManager.AUTH_TOKEN_MOCK,
        )
        # updated
        token = auth_user.auth_token
        assert eureka.logic.auth.AuthManager.update_auth_token(auth_user)
        assert auth_user.auth_token !=\
            eureka.logic.auth.AuthManager.AUTH_TOKEN_MOCK
        assert token != auth_user.auth_token
        # not updated
        token = auth_user.auth_token
        assert not \
            eureka.logic.auth.AuthManager.update_auth_token(auth_user)
        assert token == auth_user.auth_token

    def test__register(
            self, session_scope, manager,
            email, password
    ):
        """
        Register - OK
        """
        manager.register(email, password)
        # check
        with session_scope() as session:
            auth_password = session.query(
                eureka.model.auth.AuthPassword).join(
                    eureka.model.auth.AuthUser).filter(
                        eureka.model.auth.AuthUser.email == email,
                    ).one()
            assert eureka.tools.crypto.Crypto.validate_passphrase(
                password, auth_password.hashed, auth_password.salt)

    def test__register__invalid_args(self, manager, email):
        """
        Register - invalid args
        """
        with pytest.raises(eureka.logic.exc.InvalidArgument) as ex_info:
            manager.register('', '')
        assert ex_info.value.message == \
            'Invalid argument "email": ":empty:"'
        #
        with pytest.raises(eureka.logic.exc.InvalidArgument) as ex_info:
            manager.register(None, '')
        assert ex_info.value.message == \
            'Invalid argument "email": ":empty:"'
        #
        with pytest.raises(eureka.logic.exc.InvalidArgument) as ex_info:
            manager.register('e' * 255, '')
        assert ex_info.value.message == \
            'Invalid argument "email": ":too long:"'
        #
        with pytest.raises(eureka.logic.exc.InvalidArgument) as ex_info:
            manager.register('invalid', '')
        assert ex_info.value.message == \
            'Invalid argument "email": "invalid"'

    def test__register__email_exists(
            self, session_scope, manager,
            email, password
    ):
        """
        Register - email exists
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
        with pytest.raises(eureka.logic.auth.AuthError) as ex_info:
            manager.register(email, password)
        assert ex_info.value.message == \
            'Auth email "{}" already exists'.format(email)

    def test__get_auth_token(
            self, session_scope, manager,
            email, password
    ):
        """
        Get auth token - OK
        """
        hashed, salt = eureka.tools.crypto.Crypto.hash_passphrase(password)
        #
        with session_scope() as session:
            auth_user = eureka.model.auth.AuthUser(
                email=email,
                auth_token=eureka.logic.auth.AuthManager.AUTH_TOKEN_MOCK,
            )
            session.add(auth_user)
            session.flush()
            auth_password = eureka.model.auth.AuthPassword(
                auth_id=auth_user.id, hashed=hashed, salt=salt)
            session.add(auth_password)
            session.flush()
        # some token
        token = manager.get_auth_token(email, password)
        assert len(token) == eureka.tools.crypto.Crypto.auth_token_length
        assert token != eureka.logic.auth.AuthManager.AUTH_TOKEN_MOCK

    def test__get_auth_token__invalid_args(self, manager):
        """
        Get auth token - invalid args
        """
        with pytest.raises(eureka.logic.exc.InvalidArgument) as ex_info:
            manager.get_auth_token('', '')
        assert ex_info.value.message == \
            'Invalid argument "email": ":empty:"'
        #
        with pytest.raises(eureka.logic.exc.InvalidArgument) as ex_info:
            manager.get_auth_token(None, '')
        assert ex_info.value.message == \
            'Invalid argument "email": ":empty:"'
        #
        with pytest.raises(eureka.logic.exc.InvalidArgument) as ex_info:
            manager.get_auth_token('e' * 255, '')
        assert ex_info.value.message == \
            'Invalid argument "email": ":too long:"'

    def test__get_auth_token__email_not_exists(
            self, manager,
            email, password
    ):
        """
        Get auth token - email not exists
        """
        with pytest.raises(eureka.logic.auth.NotExists) as ex_info:
            manager.get_auth_token(email, password)
        assert str(ex_info.value) == \
            'Auth email "{}" not exists'.format(email)

    def test__get_auth_token__invalid_password(
            self, session_scope, manager,
            email, password
    ):
        """
        Get auth token - invalid password
        """
        hashed, salt = eureka.tools.crypto.Crypto.hash_passphrase(password)
        #
        with session_scope() as session:
            auth_user = eureka.model.auth.AuthUser(
                email=email,
                auth_token=eureka.logic.auth.AuthManager.AUTH_TOKEN_MOCK,
            )
            session.add(auth_user)
            session.flush()
            auth_password = eureka.model.auth.AuthPassword(
                auth_id=auth_user.id, hashed=hashed, salt=salt)
            session.add(auth_password)
            session.flush()
        #
        with pytest.raises(eureka.logic.auth.AuthError) as ex_info:
            manager.get_auth_token(email, 'invalid')
        assert str(ex_info.value) == \
            'invalid password'

    def test__get_auth_token__tokens_equal(
            self, session_scope, manager,
            email, password
    ):
        """
        test if simple auth exists
        """
        hashed, salt = eureka.tools.crypto.Crypto.hash_passphrase(password)
        #
        with session_scope() as session:
            auth_user = eureka.model.auth.AuthUser(
                email=email,
                auth_token=eureka.logic.auth.AuthManager.AUTH_TOKEN_MOCK,
            )
            session.add(auth_user)
            session.flush()
            auth_password = eureka.model.auth.AuthPassword(
                auth_id=auth_user.id, hashed=hashed, salt=salt)
            session.add(auth_password)
            session.flush()
        # check equal
        token_1 = manager.get_auth_token(email, password)
        token_2 = manager.get_auth_token(email, password)
        assert len(token_1) == eureka.tools.crypto.Crypto.auth_token_length
        assert token_1 == token_2
