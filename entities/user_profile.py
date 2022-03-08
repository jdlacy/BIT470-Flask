class UserProfile:

    def __init__(self, user_id=None, name="Anonymous", heading="", description="", profile_pic_url=""):
        self.user_id, self.name, self.heading, self.description, self.profile_pic_url \
            = user_id, name, heading, description, profile_pic_url

    def to_dict(self):
        return {
            "user_id": self.user_id,
            "name": self.name,
            "heading": self.heading,
            "description": self.description,
            "profile_pic_url": self.profile_pic_url
        }

    def from_dict(self, dic):
        if not (type(dic) is dict):
            raise "Requires dict as input"
        if 'user_id' in dic and 'name' in dic and 'date_joined' in dic:
            self.user_id, self.name, self.heading, self.description, self.profile_pic_url \
                = dic['user_id'], dic['name'], dic['heading'], dic['description'], dic['profile_pic_url']
