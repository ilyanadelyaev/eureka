import eureka.model.user


class TestAPIUser:
    def test__users(
            self, web_app,
            session_scope, user_name, user_email
    ):
        with session_scope() as session:
            eureka.model.user.User.query.delete()  # clear
            #
            user = eureka.model.user.User(
                name=user_name,
                email=user_email,
            )
            session.add(user)
            session.flush()
        #
        resp = web_app.get(
            '/api/user/'
        )
        assert resp.status_code == 200
        #
        assert resp.json['count'] == 1
        assert resp.json['objects'][0]['name'] == user_name
        assert resp.json['objects'][0]['email'] == user_email

    def test__users__post(self, web_app):
        resp = web_app.post(
            '/api/user/',
            expect_errors=True
        )
        assert resp.status_code == 405
