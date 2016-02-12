import eureka.model.user


class TestUserManager:
    def test__all(
            self, controller,
            session_scope, user_name, user_email,
    ):
        """
        All users
        """
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
        objs = controller.user.all()
        #
        assert len(objs) == 1
        assert objs[0]['name'] == user_name
        assert objs[0]['email'] == user_email
