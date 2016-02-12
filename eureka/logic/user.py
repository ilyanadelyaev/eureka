import validate_email

import sqlalchemy.exc
import sqlalchemy.orm.exc

import eureka.model.user


class UserError(Exception):
    pass


class InvalidArgument(UserError):
    def __init__(self, arg, val):
        super(InvalidArgument, self).__init__(
            'Invalid argument "{}": "{}"'.format(arg, val))


class AlreadyExists(UserError):
    def __init__(self):
        super(AlreadyExists, self).__init__(
            'User with given email already exists')


class NotExists(UserError):
    def __init__(self, pk):
        super(NotExists, self).__init__(
            'User "{}" is not exists'.format(pk))


class UserManager(object):
    """
    User manager
    """

    def __init__(self, db_engine):
        self.db_engine = db_engine

    @staticmethod
    def __validate_name(name):
        """
        raises on error
        """
        if not name:
            raise InvalidArgument('name', name)

    @staticmethod
    def __validate_email(email):
        """
        raises on error
        """
        if not email or not validate_email.validate_email(email):
            raise InvalidArgument('email', email)

    def create(self, data):
        """
        Create new user
        return obj_id
        raises on error
        """
        if not data:
            raise UserError('Invalid data')
        name = data.get('name', '')
        email = data.get('email', '')
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
            raise AlreadyExists()

    def update(self, pk, data):
        """
        Update existing user
        raises on error
        """
        if not data:
            raise UserError('Invalid data')
        name = data.get('name', '')
        email = data.get('email', '')
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
                ).filter_by(id=pk).one()
                if name:
                    obj.name = name
                if email:
                    obj.email = email
                session.add(obj)
                session.flush()
        except sqlalchemy.orm.exc.NoResultFound:
            raise NotExists(pk)

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
                ).filter_by(id=pk).one()
                # delete
                session.query(
                    eureka.model.user.User
                ).filter_by(id=pk).delete()
                session.flush()
        except sqlalchemy.orm.exc.NoResultFound:
            raise NotExists(pk)

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

    def all(self):
        """
        Get all users
        return [{obj}, ...]
        """
        with self.db_engine.session_scope() as session:
            return [o.to_dict() for o in session.query(
                eureka.model.user.User).all()]
