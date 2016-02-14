import logging

import validate_email

import sqlalchemy.exc
import sqlalchemy.orm.exc

import eureka.tools.retry

import eureka.logic.base
import eureka.logic.exc
import eureka.model.auth


logger = logging.getLogger('eureka')


class AuthError(eureka.logic.exc.LogicError):
    pass


class AlreadyExists(AuthError):
    def __init__(self, email):
        super(AlreadyExists, self).__init__(
            'Auth "{}" already exists'.format(email))


class NotExists(AuthError):
    def __init__(self, email):
        super(NotExists, self).__init__(
            'Auth "{}" not exists'.format(email))


class AuthManager(eureka.logic.base.ManagerBase):
    """
    Auth manager
    """

    # fill empty auth token with zeros
    # to prevent db fragmentation on future insert real auth token
    AUTH_TOKEN_MOCK = \
        '\0' * eureka.model.auth.AuthUser.auth_token.\
        property.columns[0].type.length

    @staticmethod
    def __validate_email(email):
        """
        validate email is correct
        validate email length bounds: (0..max_length]
        raises on error
        """
        if not email:
            raise eureka.logic.exc.InvalidArgument('email', email)
        # way to get max field length
        if len(email) > \
                eureka.model.auth.AuthUser.email.\
                property.columns[0].type.length:
            raise eureka.logic.exc.InvalidArgument('email', ':too long:')
        #
        if not validate_email.validate_email(email):
            raise eureka.logic.exc.InvalidArgument('email', email)

    @staticmethod
    def __validate_password(password):
        """
        Some security restrictions here
        """

    @classmethod
    def update_auth_token(cls, obj):
        """
        DUMMUY
        Check TTL for auth_token
        Update if needed
        return True for update
        """
        # not so fast but now its dummy
        # and will be replaced with ttl stuff on production
        if obj.auth_token == cls.AUTH_TOKEN_MOCK:
            obj.auth_token = eureka.tools.crypto.Crypto.generate_auth_token()
            # check here for TTL and so on
            return True
        return False

    # rewrite it to specific errors
    # TimeoutError
    @eureka.tools.retry.retry((sqlalchemy.exc.SQLAlchemyError,), logger=logger)
    def register(self, email, password):
        """
        add simple auth record
        raises on invalid or non-unique email
        """
        # validate email and password - raises on error
        self.__validate_email(email)
        self.__validate_password(password)
        # hash token to store in db
        hashed, salt = eureka.tools.crypto.Crypto.hash_passphrase(password)
        # connect to database and start transaction
        try:
            with self.db_engine.session_scope() as session:
                # Fill auth_key with mock to prevent db fragmentation
                auth_user = eureka.model.auth.AuthUser(
                    email=email,
                    auth_token=self.AUTH_TOKEN_MOCK,
                )
                session.add(auth_user)
                session.flush()  # make insert to get auth_user.id
                #
                auth_password = eureka.model.auth.AuthPassword(
                    auth_id=auth_user.id,
                    hashed=hashed,
                    salt=salt,
                )
                session.add(auth_password)
                session.flush()
        except sqlalchemy.exc.IntegrityError:
            raise AlreadyExists(email)
        #
        logger.debug('Insert "%s"', email)

    # rewrite it to specific errors
    # TimeoutError
    @eureka.tools.retry.retry((sqlalchemy.exc.SQLAlchemyError,), logger=logger)
    def get_auth_token(self, email, password):
        """
        get token via sipmle auth
        raises on errors
        """
        # validate email - raises on error
        self.__validate_email(email)
        # connect to database and start transaction
        try:
            _auth_token = None
            with self.db_engine.session_scope() as session:
                # get id and simple records
                # using SELECT .. FOR UPDATE to prevent
                # simultaneously auth_token updates
                auth_user, auth_password = session.query(
                    eureka.model.auth.AuthUser,
                    eureka.model.auth.AuthPassword
                ).join(eureka.model.auth.AuthPassword).filter(
                    eureka.model.auth.AuthUser.email == email
                ).with_for_update(read=False).one()
                # validate specified password and db data - raises on error
                if not eureka.tools.crypto.Crypto.validate_passphrase(
                        password, auth_password.hashed, auth_password.salt):
                    raise AuthError('Invalid password')
                # update auth_token if needed
                if self.update_auth_token(auth_user):
                    session.add(auth_user)
                    session.flush()
                    logger.debug(
                        'Update auth_token for "%s": %s',
                        email, auth_user.auth_token
                    )
                _auth_token = auth_user.auth_token
            #
            return _auth_token
        #
        except sqlalchemy.orm.exc.NoResultFound:
            raise NotExists(email)

    # rewrite it to specific errors
    # TimeoutError
    @eureka.tools.retry.retry((sqlalchemy.exc.SQLAlchemyError,), logger=logger)
    def get_id_by_token(self, auth_token):
        """
        get auth id via auth_token
        raises on errors
        """
        try:
            with self.db_engine.session_scope() as session:
                auth_user = session.query(
                    eureka.model.auth.AuthUser
                ).filter_by(auth_token=auth_token).one()
                return auth_user.id
        #
        except sqlalchemy.orm.exc.NoResultFound:
            raise NotExists(':auth_token:')
