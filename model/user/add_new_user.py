from model.api import Api


class AddNewUser:
    _end_point = "/registration/user/"

    def __init__(self, *args, **kwargs):
        self.args = args
        self.data = kwargs

    @property
    def to_json(self):
        return self.data

    def post(self):
        api = Api()
        response_code, response_data = api.post(self)
        return response_code, response_data
