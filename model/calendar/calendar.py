from model.api import Api


class Calendar:
    _end_point = "/calendar/"

    def __init__(self, *args, **kwargs):
        self.args = args
        self.data = kwargs
        self.dates = []

    @property
    def to_json(self):
        return self.data

    def get(self):
        api = Api()
        response_code, response_data = api.get(self)
        if response_code < 399:
            self.dates = response_data
        return response_code, response_data

    def put(self):
        api = Api()
        response_code, response_data = api.put(self)
        return response_code, response_data
