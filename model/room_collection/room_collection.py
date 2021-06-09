from model.api import Api
from model.models import Model


class RoomCollection(Model):
    _end_point = "/room_collection/"

    def __init__(self, inventory_id=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if inventory_id:
            self.query_param = {"inventory_id": inventory_id}

# class RoomCollection:
#     _end_point = "/room_collection/"
#
#     def __init__(self, inventory_id=None, *args, **kwargs):
#         if inventory_id:
#             self._end_point = f"/room_collection/?inventory_id={inventory_id}"
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
#         return response_code, response_data
#
#     def delete(self):
#         api = Api()
#         response_code, response_data = api.delete(self)
#         return response_code, response_data
