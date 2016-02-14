import eureka.tools.crypto
import eureka.model.auth
import eureka.logic.auth


class TestAPIAuth:
    def test__signup__post_201(
            self, web_app,
            session_scope,
            email, password,
    ):
        """
        Signup - OK
        """
        # clean
        with session_scope() as session:
            eureka.model.auth.AuthPassword.query.delete()
        #
        resp = web_app.post_json(
            '/api/auth/signup',
            {'email': email, 'password': password},
            expect_errors=True
        )
        assert resp.status_code == 201
        assert resp.json['result'] == 'OK'
        #
        with session_scope() as session:
            auth_user, auth_password = session.query(
                eureka.model.auth.AuthUser,
                eureka.model.auth.AuthPassword
            ).join(eureka.model.auth.AuthPassword).filter(
                eureka.model.auth.AuthUser.email == email
            ).one()
            assert eureka.tools.crypto.Crypto.validate_passphrase(
                password, auth_password.hashed, auth_password.salt)

    def test__signup__post_409(
            self, web_app,
            session_scope,
            email, password,
    ):
        """
        Signup - Already exists
        """
        hashed, salt = eureka.tools.crypto.Crypto.hash_passphrase(password)
        #
        with session_scope() as session:
            auth_user = eureka.model.auth.AuthUser(
                email=email,
            )
            session.add(auth_user)
            session.flush()
            #
            auth_password = eureka.model.auth.AuthPassword(
                auth_id=auth_user.id,
                hashed=hashed,
                salt=salt,
            )
            session.add(auth_password)
            session.flush()
        #
        resp = web_app.post_json(
            '/api/auth/signup',
            {'email': email, 'password': password},
            expect_errors=True
        )
        assert resp.status_code == 409
        assert resp.json['error'] == \
            'Auth "{}" already exists'.format(email)

    def test__signup__post_404(
            self, web_app,
            email,
    ):
        """
        Signup - error
        """
        resp = web_app.post_json(
            '/api/auth/signup',
            {},
            expect_errors=True
        )
        assert resp.status_code == 404
        assert resp.json['error'] == \
            'Invalid data'
        #
        resp = web_app.post_json(
            '/api/auth/signup',
            {'email': ''},
            expect_errors=True
        )
        assert resp.status_code == 404
        assert resp.json['error'] == \
            'Invalid argument "email": ":empty:"'
        #
        resp = web_app.post_json(
            '/api/auth/signup',
            {'email': None},
            expect_errors=True
        )
        assert resp.status_code == 404
        assert resp.json['error'] == \
            'Invalid argument "email": ":empty:"'
        #
        resp = web_app.post_json(
            '/api/auth/signup',
            {'email': 'e'*255},
            expect_errors=True
        )
        assert resp.status_code == 404
        assert resp.json['error'] == \
            'Invalid argument "email": ":too long:"'
        #
        resp = web_app.post_json(
            '/api/auth/signup',
            {'email': 'invalid'},
            expect_errors=True
        )
        assert resp.status_code == 404
        assert resp.json['error'] == \
            'Invalid argument "email": "invalid"'

    def test__signup__get_405(
            self, web_app,
    ):
        """
        Signup - not allowed
        """
        resp = web_app.get(
            '/api/auth/signup',
            expect_errors=True
        )
        assert resp.status_code == 405

    def test__signin__post_200(
            self, web_app,
            session_scope,
            email, password,
    ):
        """
        Signin - OK
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
            #
            auth_password = eureka.model.auth.AuthPassword(
                auth_id=auth_user.id,
                hashed=hashed,
                salt=salt,
            )
            session.add(auth_password)
            session.flush()
        #
        resp = web_app.post_json(
            '/api/auth/signin',
            {'email': email, 'password': password},
        )
        assert resp.status_code == 200
        assert resp.json['result'] == 'OK'
        #
        with session_scope() as session:
            auth_user = session.query(
                eureka.model.auth.AuthUser
            ).filter(
                eureka.model.auth.AuthUser.email == email
            ).one()
            assert set(resp.headers.dict_of_lists()['set-cookie']) == \
                set((
                    'auth_email="{}"; Path=/'.format(auth_user.email),
                    'auth_token={}; Path=/'.format(auth_user.auth_token),
                ))

    def test__signin__post_404_not_exists(
            self, web_app,
            email, password
    ):
        """
        Signin - error - not exists
        """
        resp = web_app.post_json(
            '/api/auth/signin',
            {'email': email, 'password': password},
            expect_errors=True
        )
        assert resp.status_code == 404
        assert resp.json['error'] == \
            'Auth "{}" not exists'.format(email)

    def test__signin__post_404_invalid_password(
            self, web_app,
            session_scope,
            email, password,
    ):
        """
        Signin - error - invalid password
        """
        hashed, salt = eureka.tools.crypto.Crypto.hash_passphrase(password)
        #
        with session_scope() as session:
            auth_user = eureka.model.auth.AuthUser(
                email=email,
            )
            session.add(auth_user)
            session.flush()
            #
            auth_password = eureka.model.auth.AuthPassword(
                auth_id=auth_user.id,
                hashed=hashed,
                salt=salt,
            )
            session.add(auth_password)
            session.flush()
        #
        resp = web_app.post_json(
            '/api/auth/signin',
            {'email': email, 'password': 'invalid'},
            expect_errors=True
        )
        assert resp.status_code == 404
        assert resp.json['error'] == 'Invalid password'

    def test__signin__post_404_invalid_args(
            self, web_app,
    ):
        """
        Signin - error - invalid args
        """
        resp = web_app.post_json(
            '/api/auth/signin',
            {},
            expect_errors=True
        )
        assert resp.status_code == 404
        assert resp.json['error'] == \
            'Invalid data'
        #
        resp = web_app.post_json(
            '/api/auth/signin',
            {'email': ''},
            expect_errors=True
        )
        assert resp.status_code == 404
        assert resp.json['error'] == \
            'Invalid argument "email": ":empty:"'
        #
        resp = web_app.post_json(
            '/api/auth/signin',
            {'email': None},
            expect_errors=True
        )
        assert resp.status_code == 404
        assert resp.json['error'] == \
            'Invalid argument "email": ":empty:"'
        #
        resp = web_app.post_json(
            '/api/auth/signin',
            {'email': 'e'*255},
            expect_errors=True
        )
        assert resp.status_code == 404
        assert resp.json['error'] == \
            'Invalid argument "email": ":too long:"'
        #
        resp = web_app.post_json(
            '/api/auth/signin',
            {'email': 'invalid'},
            expect_errors=True
        )
        assert resp.status_code == 404
        assert resp.json['error'] == \
            'Invalid argument "email": "invalid"'

    def test__signin__get_405(
            self, web_app,
    ):
        """
        Signin - not allowed
        """
        resp = web_app.get(
            '/api/auth/signin',
            expect_errors=True
        )
        assert resp.status_code == 405
