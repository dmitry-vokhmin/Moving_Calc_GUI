from model.api import Api
from model.models import Model


class User(Model):
    _end_point = "/user/"

    def get(self):
        api = Api()
        response_code, response_data = api.get(self)
        if response_code < 399:
            self.set_attr(response_data)
        return response_code, response_data

    def set_attr(self, data):
        for key, value in data.items():
            setattr(self, key, value)


# class User:
#     _end_point = "/user/"
#
#     def __init__(self, *args, **kwargs):
#         self.args = args
#         self.data = kwargs
#
#     @property
#     def to_json(self):
#         return self.data
#
#     def get(self):
#         api = Api()
#         response_code, response_data = api.get(self)
#         if response_code < 399:
#             self.set_attr(response_data)
#         return response_code, response_data
#
#     def put(self):
#         api = Api()
#         response_code, response_data = api.put(self)
#         return response_code, response_data
#
#     def delete(self):
#         api = Api()
#         response_code, response_data = api.delete(self)
#         return response_code, response_data
#
#     def set_attr(self, data):
#         for key, value in data.items():
#             setattr(self, key, value)
