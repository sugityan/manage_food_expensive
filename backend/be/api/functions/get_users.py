from db import session
from model import *


def get_users_dict():
    users_dict = {}
    users_list = session.query(UserTable).all()
    for user in users_list:
        email = user.Email
        users_dict[email] = user.toDict()
    return users_dict