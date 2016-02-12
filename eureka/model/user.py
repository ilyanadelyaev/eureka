import sqlalchemy

import eureka.database.base


class User(eureka.database.base.BaseModel):
    """
    Users
    """

    __tablename__ = 'users'

    id = sqlalchemy.Column(
        sqlalchemy.Integer,
        primary_key=True,
    )
    name = sqlalchemy.Column(
        sqlalchemy.String(60),
    )
    email = sqlalchemy.Column(
        sqlalchemy.String(150),
        unique=True,
    )

    def to_dict(self):
        """
        https://gist.github.com/alanhamlett/6604662
        """
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
        }
