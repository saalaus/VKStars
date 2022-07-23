import sqlalchemy as sa
from sqlalchemy.sql.expression import desc
from sqlalchemy.sql.functions import func

from .base import BaseModel


class User(BaseModel):
    id = sa.Column(sa.Integer, primary_key=True)
    score = sa.Column(sa.Integer, default=0)

    def get_or_create(self, session) -> "User":
        user = session.merge(self)
        if not user.score:
            user.score = 0
        return user

    @classmethod
    def get_top_10(cls, session) -> list[list[int, int]]:
        """Get top 10 users
           return list [[id, score], [id, score], ...] 
        """
        users = session.query(cls).order_by(desc(cls.score)).limit(10)
        return [ [user.id, user.score] for user in users]

    @classmethod
    def get_all(cls, session) -> dict[str, str]:
        """Get all users
        return dict {id: score}
        """
        places = func.row_number().over(order_by=desc(cls.score)).label("place")
        users: list[tuple["User", int]] = (
            session
            .query(cls)
            .order_by(desc(cls.score))
            .limit(1000)
            .add_column(places)
            )
        return {
            str(user.id): f"{user.score}_{place}"
            for user, place in users
            }
