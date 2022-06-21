from database.schemas.user import User
from loader import config
from typing import Union


def filter_post(session, signer_id: int):
    user = User(id=signer_id).get_or_create(session)
    user.score += config.table.scores.for_post


def filter_like_add(session, user_id: int):
    user: User = User(id=user_id).get_or_create(session)
    user.score += config.table.scores.for_like

def filter_like_remove(session, user_id):
    user: User = User(id=user_id).get_or_create(session)
    user.score -= config.table.scores.for_like


def filter_repost(session, user_id):
    user = User(id=user_id).get_or_create(session)
    user.score += config.table.scores.for_repost


def filter_comment_add(session, user_id, text, in_thread=False):
    score = config.table.scores.for_thread_comment\
        if in_thread else config.table.scores.for_comment

    if not config.table.meaningful_comments \
        or len(text) < config.table.meaningful_comments_min_length:
        return
    user = User(id=user_id).get_or_create(session)
    user.score += score

def filter_comment_delete(session, user_id):
    user = User(id=user_id).get_or_create(session)
    user.score -= config.table.scores.for_thread_comment

def filter_subscribe(session, user_id):
    user: User = User(id=user_id).get_or_create(session)
    user.score += config.table.scores.for_subscribe
