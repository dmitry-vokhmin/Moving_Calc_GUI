from model.api import Api
from model.models import Model


class InventoryCategory(Model):
    _end_point = "/inventory_category/"

    def __init__(self, room_id=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if room_id:
            self.query_param = {"room_id": room_id}


# class InventoryCategory:
#     _end_point = "/inventory_category/"
#
#     def __init__(self, room_id=None, *args, **kwargs):
#         if room_id:
#             self._end_point = f"/inventory_category/?room_id={room_id}"
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
