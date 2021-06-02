from model.api import Api


class UserCompany:
    _end_point = "/user/company/"

    def __init__(self):
        self.users = []

    def get(self):
        api = Api()
        response_code, response_data = api.get(self)
        if response_code < 399:
            self.users = response_data
        return response_code, response_data
