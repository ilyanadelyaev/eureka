import eureka.logic.auth
import eureka.logic.user
import eureka.logic.article


class Controller(object):
    """
    Logic controller
    """

    def __init__(self, db_engine):
        self.auth = eureka.logic.auth.AuthManager(db_engine)
        self.user = eureka.logic.user.UserManager(db_engine)
        self.article = eureka.logic.article.ArticleManager(db_engine)
