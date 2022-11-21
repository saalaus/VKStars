from database.schemas.user import User
from data import settings


def _get_or_create_user_and_add_score(session, user_id: int, score: int):
    user = User(id=user_id).get_or_create(session)
    user.score += score


def filter_post(session, signer_id: int):
    _get_or_create_user_and_add_score(
        session, signer_id, settings.FOR_POST
        )
    
def filter_post_delete(session, user_id):
    _get_or_create_user_and_add_score(
        session, user_id, -settings.FOR_POST
        )


def filter_like_add(session, user_id: int):
    _get_or_create_user_and_add_score(
        session, user_id, settings.FOR_LIKE
        )

def filter_like_remove(session, user_id):
    _get_or_create_user_and_add_score(
        session, user_id, -settings.FOR_LIKE
        )


def filter_repost(session, user_id):
    _get_or_create_user_and_add_score(
        session, user_id, settings.FOR_REPOST
        )
    
def filter_repost_delete(session, user_id):
    _get_or_create_user_and_add_score(
        session, user_id, -settings.FOR_REPOST
        )


def filter_comment_add(session, user_id, text, in_thread=False):
    score = settings.FOR_THREAD_COMMENT\
        if in_thread else settings.FOR_COMMENT

    if not settings.MEANINGFUL_COMMENTS \
        or len(text) < settings.MEANINGFUL_COMMENTS_MIN_LENGTH:
        return
    _get_or_create_user_and_add_score(
        session, user_id, score
        )

def filter_comment_delete(session, user_id):
    _get_or_create_user_and_add_score(
        session, user_id, -settings.FOR_COMMENT
        )

def filter_subscribe(session, user_id):
    _get_or_create_user_and_add_score(
        session, user_id, settings.FOR_SUBSCRIBE
        )

def filter_unsubscribe(session, user_id):
    _get_or_create_user_and_add_score(
        session, user_id, -settings.FOR_SUBSCRIBE
        )