from model.api import Api
from model.models import Model


class MoverAmount(Model):
    _end_point = "/mover_amount/"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.movers = []

    def get(self):
        api = Api()
        response_code, response_data = api.get(self)
        if response_code < 399:
            self.movers = response_data
        return response_code, response_data


# class MoverAmount:
#     _end_point = "/mover_amount/"
#
#     def __init__(self, *args, **kwargs):
#         self.args = args
#         self.data = kwargs
#         self.movers = []
#
#     @property
#     def to_json(self):
#         return self.data
#
#     def get(self):
#         api = Api()
#         response_code, response_data = api.get(self)
#         if response_code < 399:
#             self.movers = response_data
#         return response_code, response_data
#
#     def put(self):
#         api = Api()
#         response_code, response_data = api.put(self)
#         return response_code, response_data
