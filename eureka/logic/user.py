import logging

import validate_email

import sqlalchemy.exc
import sqlalchemy.orm.exc

import eureka.tools.retry

import eureka.logic.base
import eureka.model.user


logger = logging.getLogger('eureka')


class UserError(eureka.logic.exc.LogicError):
    pass


class AlreadyExists(UserError):
    def __init__(self, email):
        super(AlreadyExists, self).__init__(
            'User with email "{}" already exists'.format(email))


class NotExists(UserError):
    def __init__(self, pk):
        super(NotExists, self).__init__(
            'User "{}" is not exists'.format(pk))


class UserManager(eureka.logic.base.ManagerBase):
    """
    User manager
    """

    @staticmethod
    def __validate_name(name):
        """
        validate name length bounds: (0..max_length]
        raises on error
        """
        if not name:
            raise eureka.logic.exc.InvalidArgument('name', name)
        # way to get max field length
        if len(name) > \
                eureka.model.user.User.name.\
                property.columns[0].type.length:
            raise eureka.logic.exc.InvalidArgument('name', ':too long:')

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
                eureka.model.user.User.email.\
                property.columns[0].type.length:
            raise eureka.logic.exc.InvalidArgument('email', ':too long:')
        #
        if not validate_email.validate_email(email):
            raise eureka.logic.exc.InvalidArgument('email', email)

    # rewrite it to specific errors
    # TimeoutError
    @eureka.tools.retry.retry((sqlalchemy.exc.SQLAlchemyError,), logger=logger)
    def create(self, name, email):
        """
        Create new user
        return obj_id
        raises on error
        """
        #
        self.__validate_name(name)
        self.__validate_email(email)
        #
        _user_id = None
        try:
            with self.db_engine.session_scope() as session:
                user = eureka.model.user.User(
                    name=name,
                    email=email,
                )
                session.add(user)
                session.flush()
                _user_id = user.id
            return _user_id
        except sqlalchemy.exc.IntegrityError:
            raise AlreadyExists(email)

    # rewrite it to specific errors
    # TimeoutError
    @eureka.tools.retry.retry((sqlalchemy.exc.SQLAlchemyError,), logger=logger)
    def update(self, pk, name=None, email=None):
        """
        Update existing user
        raises on error
        """
        if not name and not email:
            raise UserError('Invalid data')
        if name:
            self.__validate_name(name)
        if email:
            self.__validate_email(email)
        try:
            with self.db_engine.session_scope() as session:
                obj = session.query(
                    eureka.model.user.User
                ).filter_by(id=pk).with_for_update(read=False).one()
                if name:
                    obj.name = name
                if email:
                    obj.email = email
                session.add(obj)
                session.flush()
        except sqlalchemy.orm.exc.NoResultFound:
            raise NotExists(pk)

    # rewrite it to specific errors
    # TimeoutError
    @eureka.tools.retry.retry((sqlalchemy.exc.SQLAlchemyError,), logger=logger)
    def delete(self, pk):
        """
        Delete user
        raises on error
        """
        try:
            with self.db_engine.session_scope() as session:
                # check existent to raise exception
                session.query(
                    eureka.model.user.User
                ).filter_by(id=pk).with_for_update(read=False).one()
                # delete
                session.query(
                    eureka.model.user.User
                ).filter_by(id=pk).delete()
                session.flush()
        except sqlalchemy.orm.exc.NoResultFound:
            raise NotExists(pk)

    # rewrite it to specific errors
    # TimeoutError
    @eureka.tools.retry.retry((sqlalchemy.exc.SQLAlchemyError,), logger=logger)
    def one(self, pk):
        """
        Get one user
        return {obj} or None
        raises on error
        """
        try:
            with self.db_engine.session_scope() as session:
                obj = session.query(
                    eureka.model.user.User
                ).filter_by(id=pk).one()
                return obj.to_dict()
        except sqlalchemy.orm.exc.NoResultFound:
            raise NotExists(pk)

    # rewrite it to specific errors
    # TimeoutError
    @eureka.tools.retry.retry((sqlalchemy.exc.SQLAlchemyError,), logger=logger)
    def all(self):
        """
        Get all users
        return [{obj}, ...]
        """
        with self.db_engine.session_scope() as session:
            return [o.to_dict() for o in session.query(
                eureka.model.user.User).all()]
