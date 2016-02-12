import eureka.logic.user


class Controller(object):
    """
    Logic controller
    """

    def __init__(self, db_engine):
        self.user = eureka.logic.user.UserManager(db_engine)
