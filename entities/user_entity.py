from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime



class User:
    # initialize class members to none
    user_id = password = date_joined = None

    # empty constructor
    def __init__(self, user_id=None, password=None, date_joined=None):
        self.user_id, self.password, self.date_joined \
            = user_id, password, date_joined

    # the below are convenience methods for converting entity to/from dictionaries

    def to_dict(self):
        return {
            "user_id": self.user_id,
            "password": self.password,
            "date_joined": self.date_joined
        }

    def from_dict(self, dic):
        if not (type(dic) is dict):
            raise "Requires dict as input"
        if 'user_id' in dic and 'password' in dic and 'date_joined' in dic:
            self.user_id, self.password, self.date_joined \
                = dic['user_id'], dic['password'], dic['date_joined']
        else:
            raise "Dictionary in UserEntity: missing required fields "


