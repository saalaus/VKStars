from flask import Flask, request
import json

import main
from const import *
import logging
logger = logging.getLogger('VKStars')
logging.basicConfig(level=logging.DEBUG)
from models import get_or_create_score


app = Flask(__name__)


@app.route("/", methods=["POST", "GET"])
def main():
    if request.data:
        data = json.loads(request.data)
    else:
        return 'ok'

    if data.get("secret") == SERVER_SECRET_KEY:
        event_type = data.get("type")
        if event_type == "confirmation":
            logger.info("return confirmation string")
            return CONFIRMATION_STRING
        elif event_type == "like_add":
            if data["object"]["object_type"] == "post":
                logger.info("like add post")
                get_or_create_score(data["object"]["liker_id"], FOR_LIKE)
        elif event_type == "like_remove":
            if data["object"]["object_type"] == "post":
                logger.info("like remove post")
                get_or_create_score(data["object"]["liker_id"], -FOR_LIKE)
        elif event_type == "wall_post_new":
            if data["object"].get("signer_id"):
                logger.info("wall post new")
                get_or_create_score(data["object"].get("signer_id"), FOR_POST)
        elif event_type == "wall_reply_new":
            if data["object"].get("reply_to_user"):
                if MEANINGFUL_COMMENTS:
                    if len(data["object"]["text"]) >= MEANINGFUL_COMMENTS_MIN_LENGTH:
                        logger.info("wall thread comment")
                        get_or_create_score(data["object"]["from_id"], FOR_THREAD_COMMENT)
                else:
                    logger.info("wall thread comment")
                    get_or_create_score(data["object"]["from_id"], FOR_THREAD_COMMENT)
            else:   
                if MEANINGFUL_COMMENTS:
                    if len(data["object"]["text"]) >= MEANINGFUL_COMMENTS_MIN_LENGTH:
                        logger.info("wall comment")
                        get_or_create_score(data["object"]["from_id"], FOR_COMMENT)
                else:
                    logger.info("wall comment")
                    get_or_create_score(data["object"]["from_id"], FOR_COMMENT)
        elif event_type == "wall_reply_edit":
            if data["object"].get("reply_to_user"):
                if MEANINGFUL_COMMENTS:
                    if len(data["object"]["text"]) < MEANINGFUL_COMMENTS_MIN_LENGTH:
                        logger.info("change thread comment -")
                        get_or_create_score(data["object"]["from_id"], -FOR_THREAD_COMMENT)
            else:
                if MEANINGFUL_COMMENTS:
                    if len(data["object"]["text"]) < MEANINGFUL_COMMENTS_MIN_LENGTH:
                        logger.info("change thread coment -")
                        get_or_create_score(data["object"]["from_id"], -FOR_COMMENT)
        elif event_type == "wall_reply_delete":
            if data["object"].get("reply_to_user"):
                logger.info("delete thread comment -")
                get_or_create_score(data["object"]["from_id"], -FOR_THREAD_COMMENT)
            else:
                logger.info("delete coment -")
                get_or_create_score(data["object"]["from_id"], -FOR_COMMENT)
        elif event_type == "wall_reply_restore":
            if MEANINGFUL_COMMENTS:
                if len(data["object"]["text"]) >= MEANINGFUL_COMMENTS_MIN_LENGTH:
                    logger.info("restore thread comment")
                    get_or_create_score(data["object"]["from_id"], FOR_THREAD_COMMENT)
                else:
                    logger.info("restore thread comment")
                    get_or_create_score(data["object"]["from_id"], FOR_THREAD_COMMENT)
            else:   
                if MEANINGFUL_COMMENTS:
                    if len(data["object"]["text"]) >= MEANINGFUL_COMMENTS_MIN_LENGTH:
                        logger.info("restore comment")
                        get_or_create_score(data["object"]["from_id"], FOR_COMMENT)
                else:
                    logger.info("restore comment")
                    get_or_create_score(data["object"]["from_id"], FOR_COMMENT)
    return 'ok'
