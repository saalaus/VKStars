from dataclasses import dataclass


@dataclass
class Group:
    id: int
    widget_token: str
    confirmation_string: str = None
    server_secret_key: str = None

@dataclass
class Scores:
    for_like: int
    for_repost: int
    for_post: int
    for_comment: int
    for_thread_comment: int
    for_subscribe: int

@dataclass
class Table:
    title: str
    scores: Scores
    meaningful_comments: bool
    meaningful_comments_min_length: int
    ignore_users: list = None


@dataclass
class Config:
    group: Group
    table: Table
    user_token: str
    api_version: float
    last_request: float = 0.0
    database_string: str = "sqlite:///test.db"


def make_config(user_token,
                api_version,
                group_id,
                widget_token,
                table_title,
                meaningful_comments,
                meaningful_comments_min_length,
                score_for_like,
                score_for_repost,
                score_for_post,
                score_for_comment,
                score_for_thread_comment,
                score_for_subscribe,
                confirmation_string=None,
                server_secret_key=None,
                ignore_users=None,
                database_string="sqlite:///test.db"
                ) -> Config:
    scores = Scores(score_for_like, score_for_repost, score_for_post,
                    score_for_comment, score_for_thread_comment,
                    score_for_subscribe)
    table = Table(table_title, scores, meaningful_comments,
                  meaningful_comments_min_length, ignore_users)
    group = Group(group_id, widget_token, confirmation_string,
                  server_secret_key)
    return Config(group, table, user_token, api_version,
                  database_string=database_string)
