from model.api import Api


class Model:
    _end_point = ""

    def __init__(self, *args, **kwargs):
        self.query_param = None
        self.args = args
        self.data = kwargs

    @property
    def to_json(self):
        return self.data

    def get(self):
        api = Api()
        response_code, response_data = api.get(self)
        return response_code, response_data

    def post(self):
        api = Api()
        response_code, response_data = api.post(self)
        return response_code, response_data

    def put(self):
        api = Api()
        response_code, response_data = api.put(self)
        return response_code, response_data

    def delete(self):
        api = Api()
        response_code, response_data = api.delete(self)
        return response_code, response_data
