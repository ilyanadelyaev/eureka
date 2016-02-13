import eureka.model.user


class TestAPIUser:
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

    def test__user__post_201(
            self, web_app,
            controller, user_name, email
    ):
        """
        Create - OK
        """
        resp = web_app.post_json(
            '/api/user/',
            {'name': user_name, 'email': email},
        )
        assert resp.status_code == 200
        #
        obj = controller.user.one(resp.json['id'])
        #
        assert obj['name'] == user_name
        assert obj['email'] == email

    def test__user__post_409(
            self, web_app,
            session_scope, user_name, email
    ):
        """
        Create - Already exists
        """
        self.__create_user(session_scope, user_name, email)
        #
        resp = web_app.post_json(
            '/api/user/',
            {'name': user_name, 'email': email},
            expect_errors=True
        )
        assert resp.status_code == 409
        #
        assert resp.json['error'] == \
            'User with email "{}" already exists'.format(email)

    def test__user__post_404(
            self, web_app,
            session_scope, user_name
    ):
        """
        Create - Error
        """
        resp = web_app.post_json(
            '/api/user/',
            {},
            expect_errors=True
        )
        assert resp.status_code == 404
        assert resp.json['error'] == \
            'Invalid data'
        #
        resp = web_app.post_json(
            '/api/user/',
            {'name': '', 'email': ''},
            expect_errors=True
        )
        assert resp.status_code == 404
        assert resp.json['error'] == \
            'Invalid argument "name": ":empty:"'
        #
        resp = web_app.post_json(
            '/api/user/',
            {'name': user_name, 'email': ''},
            expect_errors=True
        )
        assert resp.status_code == 404
        assert resp.json['error'] == \
            'Invalid argument "email": ":empty:"'
        #
        resp = web_app.post_json(
            '/api/user/',
            {'name': user_name, 'email': 'invalid'},
            expect_errors=True
        )
        assert resp.status_code == 404
        assert resp.json['error'] == \
            'Invalid argument "email": "invalid"'

    def test__users__get_list_200(
            self, web_app,
            session_scope, user_name, email
    ):
        """
        Get all - OK
        """
        self.__create_user(session_scope, user_name, email)
        #
        resp = web_app.get(
            '/api/user/',
        )
        assert resp.status_code == 200
        #
        assert resp.json['count'] == 1
        assert resp.json['objects'][0]['name'] == user_name
        assert resp.json['objects'][0]['email'] == email

    def test__user__get_200(
            self, web_app,
            session_scope, user_name, email
    ):
        """
        Read - OK
        """
        _user_id = self.__create_user(
            session_scope, user_name, email)
        #
        resp = web_app.get(
            '/api/user/{}/'.format(_user_id),
        )
        assert resp.status_code == 200
        #
        assert resp.json['name'] == user_name
        assert resp.json['email'] == email

    def test__user__get_404(
            self, web_app,
    ):
        """
        Read - Not found
        """
        resp = web_app.get(
            '/api/user/a/',
            expect_errors=True
        )
        assert resp.status_code == 404
        #
        resp = web_app.get(
            '/api/user/0/',
            expect_errors=True
        )
        assert resp.status_code == 404

    def test__user__put_200(
            self, web_app,
            controller, session_scope,
            user_name, email
    ):
        """
        Update - OK
        """
        _user_id = self.__create_user(
            session_scope, user_name, email)
        #
        resp = web_app.put_json(
            '/api/user/{}/'.format(_user_id),
            {
                'name': 'new_' + user_name,
                'email': 'new_' + email
            },
        )
        assert resp.status_code == 200
        assert resp.json['result'] == 'OK'
        #
        obj = controller.user.one(_user_id)
        assert obj['name'] == 'new_' + user_name
        assert obj['email'] == 'new_' + email

    def test__user__put_204(
            self, web_app,
    ):
        """
        Update - No content
        """
        resp = web_app.put_json(
            '/api/user/{}/'.format(0),
            {'name': '', 'email': ''},
            expect_errors=True
        )
        assert resp.status_code == 204
        #
        resp = web_app.put_json(
            '/api/user/{}/'.format(0),
            {},
            expect_errors=True
        )
        assert resp.status_code == 204

    def test__user__put_404(
            self, web_app,
            user_name, email
    ):
        """
        Update - Not found
        """
        resp = web_app.put_json(
            '/api/user/0/',
            {'name': user_name, 'email': email},
            expect_errors=True
        )
        assert resp.status_code == 404
        assert resp.json['error'] == \
            'User "0" is not exists'

    def test__user__delete_200(
            self, web_app,
            session_scope, user_name, email
    ):
        """
        Delete - OK
        """
        _user_id = self.__create_user(
            session_scope, user_name, email)
        #
        resp = web_app.delete(
            '/api/user/{}/'.format(_user_id),
        )
        assert resp.status_code == 200
        assert resp.json['result'] == 'OK'

    def test__user__delete_404(
            self, web_app,
    ):
        """
        Delete - Not found
        """
        resp = web_app.delete(
            '/api/user/0/',
            expect_errors=True
        )
        assert resp.status_code == 404
        #
        assert resp.json['error'] == \
            'User "0" is not exists'
