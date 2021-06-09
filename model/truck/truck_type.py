from model.api import Api
from model.models import Model


class TruckType(Model):
    _end_point = "/truck_type/"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.truck_types = []

    def get(self):
        api = Api()
        response_code, response_data = api.get(self)
        if response_code < 399:
            self.truck_types = response_data
        return response_code, response_data


# class TruckType:
#     _end_point = "/truck_type/"
#
#     def __init__(self, *args, **kwargs):
#         self.args = args
#         self.data = kwargs
#         self.truck_types = []
#
#     @property
#     def to_json(self):
#         return self.data
#
#     def post(self):
#         api = Api()
#         response_code, response_data = api.post(self)
#         return response_code, response_data
#
#     def get(self):
#         api = Api()
#         response_code, response_data = api.get(self)
#         if response_code < 399:
#             self.truck_types = response_data
#         return response_code, response_data
#
#     def put(self):
#         api = Api()
#         response_code, response_data = api.put(self)
#         return response_code, response_data

    def delete(self):
        api = Api()
        response_code, response_data = api.delete(self)
        return response_code, response_data
