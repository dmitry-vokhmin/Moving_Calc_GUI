from model.api import Api
from model.models import Model


class Price(Model):
    _end_point = "/price/"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.data = args
        self.kwargs = kwargs
        self.prices = []

    def get(self):
        api = Api()
        response_code, response_data = api.get(self)
        if response_code < 399:
            self.prices = response_data
        return response_code, response_data


# class Price:
#     _end_point = "/price/"
#
#     def __init__(self, *args, **kwargs):
#         self.data = args
#         self.kwargs = kwargs
#         self.prices = []
#
#     @property
#     def to_json(self):
#         return self.data
#
#     def get(self):
#         api = Api()
#         response_code, response_data = api.get(self)
#         if response_code < 399:
#             self.prices = response_data
#         return response_code, response_data
#
#     def put(self):
#         api = Api()
#         response_code, response_data = api.put(self)
#         return response_code, response_data
