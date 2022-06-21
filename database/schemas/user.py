from sqlalchemy.sql.expression import desc
from sqlalchemy.sql.functions import func
from .base import BaseModel
import sqlalchemy as sa

class User(BaseModel):
    id = sa.Column(sa.Integer, primary_key=True)
    score = sa.Column(sa.Integer, default=0)

    def get_or_create(self, session) -> "User":
        user = session.merge(self)
        if not user.score:
            user.score = 0
        return user

    @classmethod
    def get_top_10(cls, session):
        users = session.query(cls).order_by(desc(cls.score)).limit(10)
        return [[user.id, user.score] for user in users]

    @classmethod
    def get_all(cls, session):
        places = func.row_number().over(order_by=desc(cls.score)).label("place")
        users = session.execute(session.query(cls).add_column(places))
        return {str(user[0].id): str(user[0].score)+" "+str(user[1]) for user in users}