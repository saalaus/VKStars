from models import User
from pprint import pprint
import json


with open("users.txt", "r") as file:
    users = json.load(file)
    for user in users:
        User.create(user_id = user, scores = users[user])
