import eureka.model.user


class TestAPIUser:
    @staticmethod
    def __create_user(session_scope, user_name, user_email):
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
                email=user_email,
            )
            session.add(user)
            session.flush()
            _user_id = user.id
        return _user_id

    def test__user__post_201(
            self, web_app,
            controller, user_name, user_email
    ):
        """
        Create - OK
        """
        resp = web_app.post_json(
            '/api/user/',
            {'name': user_name, 'email': user_email},
        )
        assert resp.status_code == 200
        #
        obj = controller.user.one(resp.json['obj_id'])
        #
        assert obj['name'] == user_name
        assert obj['email'] == user_email

    def test__user__post_409(
            self, web_app,
            session_scope, user_name, user_email
    ):
        """
        Create - Already exists
        """
        self.__create_user(session_scope, user_name, user_email)
        #
        resp = web_app.post_json(
            '/api/user/',
            {'name': user_name, 'email': user_email},
            expect_errors=True
        )
        assert resp.status_code == 409
        #
        assert resp.json['error'] == \
            'User with given email already exists'

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
            'Invalid argument "name": ""'
        #
        resp = web_app.post_json(
            '/api/user/',
            {'name': user_name, 'email': ''},
            expect_errors=True
        )
        assert resp.status_code == 404
        assert resp.json['error'] == \
            'Invalid argument "email": ""'
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
            session_scope, user_name, user_email
    ):
        """
        Get all - OK
        """
        self.__create_user(session_scope, user_name, user_email)
        #
        resp = web_app.get(
            '/api/user/',
        )
        assert resp.status_code == 200
        #
        assert resp.json['count'] == 1
        assert resp.json['objects'][0]['name'] == user_name
        assert resp.json['objects'][0]['email'] == user_email

    def test__user__get_200(
            self, web_app,
            session_scope, user_name, user_email
    ):
        """
        Read - OK
        """
        _user_id = self.__create_user(
            session_scope, user_name, user_email)
        #
        resp = web_app.get(
            '/api/user/{}/'.format(_user_id),
        )
        assert resp.status_code == 200
        #
        assert resp.json['name'] == user_name
        assert resp.json['email'] == user_email

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
    ):
        """
        Update - OK
        """

    def test__user__put_204(
            self, web_app,
    ):
        """
        Update - No content
        """

    def test__user__put_404(
            self, web_app,
    ):
        """
        Update - Not found
        """

    def test__user__delete_200(
            self, web_app,
    ):
        """
        Delete - OK
        """

    def test__user__delete_404(
            self, web_app,
    ):
        """
        Delete - Not found
        """
