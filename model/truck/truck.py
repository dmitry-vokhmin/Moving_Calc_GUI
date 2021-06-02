from model.api import Api


class Truck:
    _end_point = "/truck/"

    def __init__(self, *args, **kwargs):
        self.args = args
        self.data = kwargs
        self.trucks = []

    @property
    def to_json(self):
        return self.data

    def post(self):
        api = Api()
        response_code, response_data = api.post(self)
        return response_code, response_data

    def get(self):
        api = Api()
        response_code, response_data = api.get(self)
        if response_code < 399:
            self.trucks = response_data
        return response_code, response_data

    def put(self):
        api = Api()
        response_code, response_data = api.put(self)
        return response_code, response_data

    def delete(self):
        api = Api()
        response_code, response_data = api.delete(self)
        return response_code, response_data
