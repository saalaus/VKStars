from collections import defaultdict

from VKmain import method
from const import *
from models import User


users_scores = defaultdict(int)


def scan_members():
    offset = 0
    post = method("groups.getMembers", group_id = abs(GROUP_ID), offset = 0, count = 1000).json()
    all_count = post["response"]["count"]
    count = 1
    while post["response"]["items"]:
        offset += 1000
        for member in post["response"]["items"]:
            print("Сканирование подписчиков: ", count, "Из", all_count)
            users_scores[str(member)] += FOR_SUBSCRIBE
            count += 1
        post = method("groups.getMembers", group_id = abs(GROUP_ID), offset = offset, count = 1000).json()


def scan_posts():
    print("Сканирование стены...")
    offset = 0
    posts = method("wall.get", owner_id = GROUP_ID, offset = 0, count = 100).json()
    all_count = posts["response"]["count"]
    count = 1
    while posts["response"]["items"]:
        offset += 100
        for post in posts["response"]["items"]:
            print("Сканирование стены: ", count, "Из", all_count)
            count += 1
            post_id = post["id"]
            if post["likes"]["count"]:
                get_likes(post_id)
            if post["comments"]["count"]:
                get_comments(post_id)
            if post["reposts"]["count"]:
                get_reposts(post_id)
            if post.get("signer_id"):
                filter_post(post["signer_id"])
        posts = method("wall.get", owner_id = GROUP_ID, offset = offset, count = 100).json()
    print("Сканирование стены завершено")



def get_likes(post_id):
    offset = 0
    post = method("likes.getList", type = "post", owner_id = GROUP_ID, item_id = post_id, filter = "likes", offset = 0, count = 100).json()
    all_count = post["response"]["count"]
    count = 1
    while post["response"]["items"]:
        offset += 100
        for like in post["response"]["items"]:
            print("    Сканирование лайков: ", count, "Из", all_count)
            filter_likes(like)
            count += 1
        post = method("likes.getList", type = "post", owner_id = GROUP_ID, item_id = post_id, filter = "likes", offset = offset, count = 100).json()


def get_reposts(post_id):
    offset = 0
    post = method("wall.getReposts", owner_id = GROUP_ID, post_id = post_id, offset = 0, count = 100).json()
    count = 1
    while post["response"]["items"]:
        offset += 100
        for repost in post["response"]["items"]:
            print("    Сканирование репостов: ", count)
            count += 1
            filter_repost(repost)
        post = method("wall.getReposts", owner_id = GROUP_ID, post_id = post_id, offset = offset, count = 100).json()


def get_comments(post_id):
    offset = 0
    post = method("wall.getComments", owner_id = GROUP_ID, post_id = post_id, offset = 0, count = 100, need_likes = True).json()
    all_count = post["response"]["count"]
    count = 1
    while post["response"]["items"]:
        for comment in post["response"]["items"]:
            print("    Сканирование комментариев: ", count, "Из", all_count)
            filter_comment(comment)
            count += 1
            if comment["thread"]["count"]:
                get_thread_comment(comment["id"])
        offset += 100
        post = method("wall.getComments", owner_id = GROUP_ID, post_id = post_id, offset = offset, count = 100, need_likes = True).json()



def get_thread_comment(comment_id):
    offset = 0
    post = method("wall.getComments", owner_id = GROUP_ID, offset = 0, count = 100, comment_id = comment_id, need_likes = True).json()
    all_count = post["response"]["count"]
    count = 1
    while post["response"]["items"]:
        offset += 100
        all_count = post["response"]["count"]
        for comment in post["response"]["items"]:
            print("        Сканирование треда: ", count, "Из", all_count)
            filter_comment(comment, in_thread = True)
            count += 1
        post = method("wall.getComments", owner_id = GROUP_ID, offset = offset, count = 100, comment_id = comment_id, need_likes = True).json()


def scan_members_execute():
    offset = 0
    code = '''var users = [];
              var i = 0;
              var group_id = {}
              var offset = {};
              var end = false;
              while (i < 25){{
                var members = API.groups.getMembers({{"group_id":group_id, "offset": offset, "count": 1000}});
                if (members.count <= offset){{
                end = true;i = 25;
                }}
                users.push(members.items);
                i = i+1;
                offset = offset+1000;
              }};
              return [end, users];'''#.format(abs(GROUP_ID),
                                             #        offset)
    members = method("execute", code = code.format(abs(GROUP_ID), offset)).json()
    for user in members[1]
    while members[0]:
        offset += 25000



def filter_post(signer_id):
    users_scores[str(signer_id)] += FOR_POST


def filter_likes(like_id):
    users_scores[str(like_id)] += FOR_LIKE


def filter_repost(repost):
    users_scores[str(repost["from_id"])] += FOR_REPOST


def filter_comment(comment, in_thread = False):
    if MEANINGFUL_COMMENTS:
        if len(comment) >= MEANINGFUL_COMMENTS_MIN_LENGTH:
            if in_thread:
                users_scores[str(comment["from_id"])] += FOR_THREAD_COMMENT
            else:
                users_scores[str(comment["from_id"])] += FOR_COMMENT
    else:
        if in_thread:
            users_scores[str(comment["from_id"])] += FOR_THREAD_COMMENT
        else:
            users_scores[str(comment["from_id"])] += FOR_COMMENT



if __name__ == "__main__":
    scan_members()
    scan_posts()
    
    for user in users_scores:
        User.create(user_id = user, scores = users_scores[user])


