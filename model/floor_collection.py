from model.models import Model
from model.api import Api


class FloorCollection(Model):
    _end_point = "/floor_collection/"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.floor_collections = []

    def get(self):
        api = Api()
        response_code, response_data = api.get(self)
        if response_code < 399:
            self.floor_collections = response_data
        return response_code, response_data
