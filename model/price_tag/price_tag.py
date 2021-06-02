from model.api import Api


class PriceTag:
    _end_point = "/price_tag/"

    def __init__(self, *args, **kwargs):
        self.args = args
        self.data = kwargs
        self.price_tags = []

    @property
    def to_json(self):
        return self.data

    def get(self):
        api = Api()
        response_code, response_data = api.get(self)
        if response_code < 399:
            self.price_tags = response_data
        return response_code, response_data
