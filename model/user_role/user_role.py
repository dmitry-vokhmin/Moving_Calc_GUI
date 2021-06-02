from model.api import Api


class UserRole:
    _end_point = "/user_role/"

    def __init__(self):
        self.children_roles = None

    def get(self):
        api = Api()
        response_code, response_data = api.get(self)
        if response_code < 399:
            self.children_roles = response_data
        return response_code, response_data
