import logging

from data import const
from data.config import make_config

config = make_config(const.USER_TOKEN, const.API_VERSION, const.GROUP_ID,
                     const.WIDGET_TOKEN, const.TITLE, const.MEANINGFUL_COMMENTS,
                     const.MEANINGFUL_COMMENTS_MIN_LENGTH, const.FOR_LIKE,
                     const.FOR_REPOST, const.FOR_POST, const.FOR_COMMENT,
                     const.FOR_THREAD_COMMENT, const.FOR_SUBSCRIBE,
                     const.CONFIRMATION_STRING, const.SERVER_SECRET_KEY,
                     const.IGNORES_USERS)

logging.basicConfig(level=logging.CRITICAL)
logger = logging.getLogger("vkstars")
logger.setLevel(logging.DEBUG)

