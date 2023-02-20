import json

from flask import Flask, request

from data import settings
from database import Session
from utils.filters import (
    filter_comment_add,
    filter_comment_delete,
    filter_like_add,
    filter_like_remove,
    filter_post,
    filter_post_delete,
    filter_repost,
    filter_repost_delete,
    filter_subscribe,
    filter_unsubscribe,
)

app = Flask(__name__)


@app.route("/", methods=["POST"])
def index():
    if not request.data:
        return 'ok'
    data = json.loads(request.data)
    if not data.get("secret") == settings.SERVER_SECRET_KEY:
        return 'ok'
    session = Session()
    event_dict = {
        "confirmation": lambda _: settings.CONFIRMATION_STRING,
        "like_add": lambda object: filter_like_add(session, object.get("liker_id")) if object.get("object_type") == "post" else None,
        "like_remove": lambda object: filter_like_remove(session, object.get("liker_id")) if object.get("object_type") == "post" else None,
        "wall_post_new": lambda object: filter_post(session, object.get("signer_id")),
        "wall_reply_new": lambda object: filter_comment_add(session, object.get("from_id"), object.get("text"), bool(object.get("reply_to_user"))),
        "wall_reply_edit": lambda object: print("edit comment"),
        "wall_reply_restore": lambda object: filter_comment_add(session, object.get("from_id")),
        "wall_reply_delete": lambda object: filter_comment_delete(session, object.get("from_id")),
        "group_join": lambda object: filter_subscribe(session, object.get("user_id")),
        "group_leave": lambda object: filter_unsubscribe(session, object.get("user_id")),
        "wall_repost": lambda object: filter_repost(session, object.get("user_id")),

    }

    event_type = data.get("type")
    func = event_dict.get(event_type)
    if not func:
        logger.error(f"No handler for {event_type}")
        return "ok"
    logger.info(f"Run handler {event_type}")
    return_data = func(data["object"])

    session.commit()
    session.close()
    logger.info(f"Return {return_data}")
    return 'ok' if not return_data else return_data
