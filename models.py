from peewee import *
import logging
logger = logging.getLogger('VKStars')
logging.basicConfig(level=logging.DEBUG)

db = SqliteDatabase("user.db")


class User(Model):
    user_id = IntegerField(unique=True)
    scores = IntegerField(default = 0)

    class Meta:
        database = db


#  получение всех пользователь из базы данных в формате {id: "scores place"}
def get_all():
    logger.info("Get all users in database")
    try:
        users = User.select(User, fn.row_number().over(order_by = User.scores.desc()).alias("place"))
        return {str(user.user_id): str(user.scores)+" "+str(user.place) for user in users}
    except Exception as e:
        logger.critical(e)


# получение топ 10 по очкам в массиве
def get_top_10():
    logger.info("Get top 10 users in database")
    try:
        users = User.select().order_by(User.scores.desc()).limit(10)
        return [[str(user.user_id), user.scores] for user in users]
    except Exception as e:
        logger.critical(e)


# получение или создание и добавление очков
def get_or_create_score(user_id, scores):
    # возвращает кортеж с пользователем и новый ли пользователь
    logger.info(f"Try get or create {user_id} and add scores {scores}")
    try: 
        user = User.get_or_create(user_id = user_id)[0]
        user.scores += scores
        logger.info("Save scores...")
        user.save()
    except Exception as e:
        logger.critical(e)
