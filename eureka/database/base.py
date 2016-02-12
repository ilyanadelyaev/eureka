import sqlalchemy
import sqlalchemy.ext.declarative
import sqlalchemy.sql


BaseModel = sqlalchemy.ext.declarative.declarative_base()


class AuditBaseModel(BaseModel):
    """
    Base model abstract with audit log
    """

    __abstract__ = True

    created_on = sqlalchemy.Column(
        sqlalchemy.DateTime,
        default=sqlalchemy.sql.func.now(),
    )
    updated_on = sqlalchemy.Column(
        sqlalchemy.DateTime,
        default=sqlalchemy.sql.func.now(),
        onupdate=sqlalchemy.sql.func.now()
    )
