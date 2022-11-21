
from database import Session
from database.schemas.user import User
from data import settings
from utils.filters import filter_comment_add, filter_like_add, filter_post, \
    filter_repost, filter_subscribe
from vk.api import method
from vk.execute import ExecuteCode


def filter_all_members(session):
    """Yield all members"""
    offset = 0
    end = False

    while not end:
        members = method("execute",
                         code=ExecuteCode.get_members.value,
                         group_id = settings.GROUP_ID,
                         offset = offset
                         )["response"]

        end = members["end"]
        for member in members["items"]:
            filter_subscribe(session, member)
        offset += 25_000
        


def scan_posts(session):
    print("Сканирование стены...")
    offset = 0
    posts = method("wall.get", owner_id=settings.GROUP_ID*-1,
                   offset=0, count=100)
    all_count = posts["response"]["count"]
    count = 1
    while posts["response"]["items"]:
        offset += 100
        for post in posts["response"]["items"]:
            print("Сканирование стены: ", count, "Из", all_count)
            count += 1
            post_id = post["id"]
            if post["likes"]["count"]:
                get_likes(session, post_id)
            if post["comments"]["count"]:
                get_comments(session, post_id)
            if post["reposts"]["count"]:
                get_reposts(session, post_id)
            if post.get("signer_id"):
                filter_post(session, post["signer_id"])
        posts = method("wall.get", owner_id=settings.GROUP_ID*-1,
                       offset=offset, count=100)
    print("Сканирование стены завершено")


def get_likes(session, post_id):
    offset = 0
    post = method("likes.getList", type="post", owner_id=settings.GROUP_ID*-1,
                  item_id=post_id, filter="likes", offset=0, count=100)
    all_count = post["response"]["count"]
    count = 1
    while post["response"]["items"]:
        offset += 100
        for like in post["response"]["items"]:
            print("    Сканирование лайков: ", count, "Из", all_count)
            filter_like_add(session, like)
            count += 1
        post = method("likes.getList", type="post",
                      owner_id=settings.GROUP_ID*-1, item_id=post_id,
                      filter="likes", offset=offset, count=100)


def get_reposts(session, post_id):
    offset = 0
    post = method("wall.getReposts", owner_id=settings.GROUP_ID*-1,
                  post_id=post_id, offset=0, count=100)
    count = 1
    while post["response"]["items"]:
        offset += 100
        for repost in post["response"]["items"]:
            print("    Сканирование репостов: ", count)
            count += 1
            filter_repost(session, repost.get("from_id"))
        post = method("wall.getReposts", owner_id=settings.GROUP_ID*-1,
                      post_id=post_id, offset=offset, count=100)


def get_comments(session, post_id):
    offset = 0
    post = method("wall.getComments", owner_id=settings.GROUP_ID*-1,
                  post_id=post_id, offset=0, count=100, need_likes=True)
    all_count = post["response"]["count"]
    count = 1
    while post["response"]["items"]:
        for comment in post["response"]["items"]:
            print("    Сканирование комментариев: ", count, "Из", all_count)
            filter_comment_add(session, comment["from_id"], comment["text"])
            count += 1
            if comment["thread"]["count"]:
                get_thread_comment(session, comment["id"])
        offset += 100
        post = method("wall.getComments", owner_id=settings.GROUP_ID*-1,
                      post_id=post_id, offset=offset, count=100,
                      need_likes=True)


def get_thread_comment(session, comment_id):
    offset = 0
    post = method("wall.getComments", owner_id=settings.GROUP_ID*-1, offset=0,
                  count=100, comment_id=comment_id, need_likes=True)
    all_count = post["response"]["count"]
    count = 1
    while post["response"]["items"]:
        offset += 100
        all_count = post["response"]["count"]
        for comment in post["response"]["items"]:
            print("        Сканирование треда: ", count, "Из", all_count)
            filter_comment_add(session, comment["from_id"], comment["text"], in_thread=True)
            count += 1
        post = method("wall.getComments", owner_id=settings.GROUP_ID*-1, offset=offset,
                      count=100, comment_id=comment_id, need_likes=True)


def main():
    with Session() as session:
        filter_all_members(session)
        scan_posts(session)
        session.commit()
if __name__ == "__main__":
    main()
