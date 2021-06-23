from model.api import Api
from model.models import Model


class UserRole(Model):
    _end_point = "/user_role/"

    def __init__(self, *args, **kwargs):
        super(UserRole, self).__init__(*args, **kwargs)
        self.children_roles = None

    def get(self):
        api = Api()
        response_code, response_data = api.get(self)
        if response_code < 399:
            self.children_roles = response_data
        return response_code, response_data
