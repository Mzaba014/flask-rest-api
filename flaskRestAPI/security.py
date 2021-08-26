import hmac
from user import User

users = [
    User(1, 'Manny', 'pass')
]

username_map = {u.username: u for u in users}  # map usernames to user objects
userid_map = {u.id: u for u in users}  # map ids to user objects


def authenticate(username, password):
    user = username_map.get(username)
    if user and hmac.compare_digest(user.password, password):
        return user


def identity(payload):
    user_id = payload['identity']
    return userid_map.get(user_id, None)
