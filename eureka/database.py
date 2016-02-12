import contextlib

import sqlalchemy
import sqlalchemy.orm
import sqlalchemy.ext.declarative


Base = sqlalchemy.ext.declarative.declarative_base()


class DBEngine(object):
    """
    Database engine controller
    """

    def __init__(self, config):
        self.engine = sqlalchemy.create_engine(
            config.db.url,
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
        Base.query = self.db_session.query_property()
        self.__ensure_tables()

    def __ensure_tables(self):
        """
        Ensure database tables
        """
        import eureka.model  # load models to get tables
        Base.metadata.create_all(bind=self.engine)

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
