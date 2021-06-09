from model.api import Api
from model.models import Model


class Registration(Model):
    _end_point = "/registration/"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


# class Registration:
#     _end_point = "/registration/"
#
#     def __init__(self, fullname, email, password):
#         self.fullname = fullname
#         self.email = email
#         self.password = password
#
#     @property
#     def to_json(self):
#         return {
#             "fullname": self.fullname,
#             "email": self.email,
#             "password": self.password
#         }
#
#     def post(self):
#         api = Api()
#         response_code, response_data = api.post(self)
#         return response_code, response_data
