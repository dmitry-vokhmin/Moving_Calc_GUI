from model.api import Api
from model.models import Model


class MoveSize(Model):
    _end_point = "/move_size/"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.move_sizes = []

    def get(self):
        api = Api()
        response_code, response_data = api.get(self)
        if response_code < 399:
            self.move_sizes = response_data
        return response_code, response_data


# class MoveSize:
#     _end_point = "/move_size/"
#
#     def __init__(self, *args, **kwargs):
#         self.args = args
#         self.data = kwargs
#         self.move_sizes = []
#
#     @property
#     def to_json(self):
#         return self.data
#
#     def get(self):
#         api = Api()
#         response_code, response_data = api.get(self)
#         if response_code < 399:
#             self.move_sizes = response_data
#         return response_code, response_data