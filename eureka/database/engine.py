import os
import contextlib

import sqlalchemy
import sqlalchemy.orm

import eureka.database.base


class DBEngine(object):
    """
    Database engine controller
    """

    def __init__(self, config):
        # get from env then from config
        db_url = os.environ.get('DATABASE_URL', None)
        if not db_url:
            db_url = config.db.url
        #
        self.engine = sqlalchemy.create_engine(
            db_url,
            convert_unicode=True,
        )
        self.db_session = sqlalchemy.orm.scoped_session(
            sqlalchemy.orm.sessionmaker(
                bind=self.engine,
                autocommit=False,
                autoflush=False,
            )
        )
        #
        eureka.database.base.BaseModel.query = \
            self.db_session.query_property()
        self.__ensure_tables()

    def __ensure_tables(self):
        """
        Ensure database tables
        """
        # pylint: disable=W0621
        import eureka.model  # load models to get tables
        eureka.database.base.BaseModel.metadata.create_all(
            bind=self.engine)

    def register_flask_callbacks(self, flask_app):
        # callback functiion
        # pylint: disable=W0612
        @flask_app.teardown_appcontext
        def teardown_appcontext(_=None):  # exception=None
            """
            - Shutdown session
            """
            # shutdown session
            self.db_session.remove()

    @contextlib.contextmanager
    def session_scope(self):
        """
        Using:
        with self.session_scope() as session:
            ...
        """
        session = self.db_session()
        try:
            yield session
            session.commit()  # and release all db locks
        except:
            session.rollback()
            raise
        finally:
            session.close()
