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


class UserManager(object):
    """
    User manager
    """

    def __init__(self, db_engine):
        self.db_engine = db_engine

    @staticmethod
    def __validate(name, email):
        """
        validate new user data
        """
        if not name:
            raise InvalidArgument('name', name)
        if not email:
            raise InvalidArgument('email', email)
        if not validate_email.validate_email(email):
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
        self.__validate(name, email)
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

    def one(self, pk):
        """
        Get one user
        return {obj} or None
        """
        try:
            with self.db_engine.session_scope() as session:
                obj = session.query(
                    eureka.model.user.User
                ).filter_by(id=pk).one()
                return obj.to_dict()
        except sqlalchemy.orm.exc.NoResultFound:
            return

    def all(self):
        """
        Get all users
        return [{obj}, ...]
        """
        with self.db_engine.session_scope() as session:
            return [o.to_dict() for o in session.query(
                eureka.model.user.User).all()]
