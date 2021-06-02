from model.api import Api


class UserPrivilege:
    _end_point = "/user_privilege/user/"

    @classmethod
    def get(cls):
        api = Api()
        response_code, response_data = api.get(cls)
        return response_code, response_data
