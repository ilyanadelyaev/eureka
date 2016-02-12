import eureka.model.user


class TestUserModel:
    def test__create(self, session_scope):
        """
        Create record in db
        """
        with session_scope() as session:
            user = eureka.model.user.User(name='name', email='email')
            session.add(user)
            session.flush()
        with session_scope() as session:
            obj = session.query(eureka.model.user.User).first()
            assert obj.name == 'name'
