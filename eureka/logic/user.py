import eureka.model.user


class UserManager(object):
    """
    User manager
    """

    def __init__(self, db_engine):
        self.db_engine = db_engine

    def all(self):
        with self.db_engine.session_scope() as session:
            return [o.to_dict() for o in session.query(
                eureka.model.user.User).all()]
