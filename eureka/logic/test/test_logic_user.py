import pytest

import eureka.model.user
import eureka.logic.user
import eureka.logic.exc


class TestUserManager:
    @staticmethod
    def __create_user(session_scope, user_name, email):
        """
        user creation helper
        """
        _user_id = None
        with session_scope() as session:
            # clear table
            eureka.model.user.User.query.delete()
            #
            user = eureka.model.user.User(
                name=user_name,
                email=email,
            )
            session.add(user)
            session.flush()
            _user_id = user.id
        return _user_id

    def test__create(
            self, controller,
            user_name, email,
    ):
        """
        Create user
        """
        obj_id = controller.user.create(user_name, email)
        #
        obj = controller.user.one(obj_id)
        assert obj['name'] == user_name
        assert obj['email'] == email

    def test__create__exists(
            self, controller,
            session_scope, user_name, email,
    ):
        """
        Create user - email exists
        """
        controller.user.create(user_name, email)
        #
        with pytest.raises(eureka.logic.user.AlreadyExists) as ex_info:
            controller.user.create(user_name, email)
        assert ex_info.value.message == \
            'User with email "{}" already exists'.format(email)

    def test__create__invalid_args(
            self, controller,
            session_scope, user_name,
    ):
        """
        Create user - raises on invalid args
        """
        with pytest.raises(eureka.logic.exc.InvalidArgument) as ex_info:
            controller.user.create(None, None)
        assert ex_info.value.message == \
            'Invalid argument "name": ":empty:"'
        #
        with pytest.raises(eureka.logic.exc.InvalidArgument) as ex_info:
            controller.user.create('', None)
        assert ex_info.value.message == \
            'Invalid argument "name": ":empty:"'
        #
        with pytest.raises(eureka.logic.exc.InvalidArgument) as ex_info:
            controller.user.create('n'*61, None)
        assert ex_info.value.message == \
            'Invalid argument "name": ":too long:"'
        #
        with pytest.raises(eureka.logic.exc.InvalidArgument) as ex_info:
            controller.user.create(user_name, None)
        assert ex_info.value.message == \
            'Invalid argument "email": ":empty:"'
        #
        with pytest.raises(eureka.logic.exc.InvalidArgument) as ex_info:
            controller.user.create(user_name, '')
        assert ex_info.value.message == \
            'Invalid argument "email": ":empty:"'
        #
        with pytest.raises(eureka.logic.exc.InvalidArgument) as ex_info:
            controller.user.create(user_name, 'e'*255)
        assert ex_info.value.message == \
            'Invalid argument "email": ":too long:"'
        #
        with pytest.raises(eureka.logic.exc.InvalidArgument) as ex_info:
            controller.user.create(user_name, 'invalid')
        assert ex_info.value.message == \
            'Invalid argument "email": "invalid"'

    def test__update__name(
            self, controller,
            session_scope, user_name, email,
    ):
        """
        Update user - name
        """
        _user_id = self.__create_user(
            session_scope, user_name, email)
        #
        controller.user.update(_user_id, name=('new_' + user_name))
        #
        obj = controller.user.one(_user_id)
        assert obj['name'] == 'new_' + user_name
        assert obj['email'] == email

    def test__update__email(
            self, controller,
            session_scope, user_name, email,
    ):
        """
        Update user - email
        """
        _user_id = self.__create_user(
            session_scope, user_name, email)
        #
        controller.user.update(_user_id, email=('new_' + email))
        #
        obj = controller.user.one(_user_id)
        assert obj['name'] == user_name
        assert obj['email'] == 'new_' + email

    def test__update__not_exists(
            self, controller,
    ):
        """
        Update user - not exists
        """
        with pytest.raises(eureka.logic.user.NotExists) as ex_info:
            controller.user.update(0, {'name': 'name'})
        assert ex_info.value.message == \
            'User "0" is not exists'

    def test__update__invalid_args(
            self, controller,
            session_scope, user_name, email,
    ):
        """
        Update user - invalid args
        """
        with pytest.raises(eureka.logic.user.UserError) as ex_info:
            controller.user.update(0, name=None)
        assert ex_info.value.message == \
            'Invalid data'
        #
        with pytest.raises(eureka.logic.user.UserError) as ex_info:
            controller.user.update(0, name='')
        assert ex_info.value.message == \
            'Invalid data'
        #
        with pytest.raises(eureka.logic.user.UserError) as ex_info:
            controller.user.update(0, email=None)
        assert ex_info.value.message == \
            'Invalid data'
        #
        with pytest.raises(eureka.logic.user.UserError) as ex_info:
            controller.user.update(0, email='')
        assert ex_info.value.message == \
            'Invalid data'
        #
        with pytest.raises(eureka.logic.exc.InvalidArgument) as ex_info:
            controller.user.update(0, email='e'*255)
        assert ex_info.value.message == \
            'Invalid argument "email": ":too long:"'
        #
        with pytest.raises(eureka.logic.exc.InvalidArgument) as ex_info:
            controller.user.update(0, email='invalid')
        assert ex_info.value.message == \
            'Invalid argument "email": "invalid"'

    def test__delete(
            self, controller,
            session_scope, user_name, email,
    ):
        """
        Delete user - OK
        """
        _user_id = self.__create_user(
            session_scope, user_name, email)
        #
        controller.user.delete(_user_id)
        #
        with pytest.raises(eureka.logic.user.NotExists):
            controller.user.one(_user_id)

    def test__delete__not_exists(
            self, controller,
            session_scope, user_name, email,
    ):
        """
        Delete user - Not exists
        """
        with pytest.raises(eureka.logic.user.NotExists):
            controller.user.delete(0)

    def test__one(
            self, controller,
            session_scope, user_name, email,
    ):
        """
        One user
        """
        _user_id = self.__create_user(
            session_scope, user_name, email)
        #
        obj = controller.user.one(_user_id)
        #
        assert obj['name'] == user_name
        assert obj['email'] == email

    def test__one__not_exists(
            self, controller,
            session_scope, user_name, email,
    ):
        """
        One user - not exists
        """
        with pytest.raises(eureka.logic.user.NotExists) as ex_info:
            controller.user.one(0)
        assert ex_info.value.message == \
            'User "0" is not exists'

    def test__all(
            self, controller,
            session_scope, user_name, email,
    ):
        """
        All users
        """
        self.__create_user(session_scope, user_name, email)
        #
        objs = controller.user.all()
        #
        assert len(objs) == 1
        assert objs[0]['name'] == user_name
        assert objs[0]['email'] == email
