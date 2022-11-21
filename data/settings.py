# user token with permissions groups, wall, likes
USER_TOKEN = "vk1.a..."


API_VERSION = "5.130"  # version API VK


GROUP_ID = 190129811  # ID groups(POSITIVE)
# group token with permissions: app_widget
WIDGET_TOKEN = "vk1.a...."
CONFIRMATION_STRING = "STRING"  # string to be returned by the server
SERVER_SECRET_KEY = "tablewidgetstarbot"  # secret key callback server


IGNORES_USERS = []  # Id users ignored
FOR_LIKE = 2  # points for like
FOR_REPOST = 10  # points for like
FOR_COMMENT = 5  # points for comment
FOR_THREAD_COMMENT = 2  # points for thread comment
FOR_POST = 15  # point for post(by signer_id)
FOR_SUBSCRIBE = 10  # points for subscribe


TITLE = "Баллы"  # Name for 3 column

# meaningful comments, only text, witout stickers and etc
MEANINGFUL_COMMENTS = True
MEANINGFUL_COMMENTS_MIN_LENGTH = 3  # minimal len text comment

DATABASE_STRING = "sqlite:///test.db"  # database string