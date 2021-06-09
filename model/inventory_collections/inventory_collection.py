from model.api import Api
from model.models import Model


class InventoryCollection(Model):
    _end_point = "/inventory_collection/"

    def __init__(self, inventory_id=None, inventory_collection_id=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if inventory_collection_id:
            self.query_param = {"inventory_collection_id": inventory_collection_id}
        elif inventory_id:
            self.data.update({"inventory_id": inventory_id})


# class InventoryCollection:
#     _end_point = "/inventory_collection/"
#
#     def __init__(self, inventory_id=None, inventory_collection_id=None, *args, **kwargs):
#         self.args = args
#         self.data = kwargs
#         if inventory_id and inventory_collection_id:
#             self._end_point = f"/inventory_collection/?inventory_id={inventory_id}&" \
#                               f"inventory_collection_id={inventory_collection_id}"
#         elif inventory_id:
#             self.data["inventory_id"] = inventory_id
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
#     def post(self):
#         api = Api()
#         response_code, response_data = api.post(self)
#         return response_code, response_data
#
#     def delete(self):
#         api = Api()
#         response_code, response_data = api.delete(self)
#         return response_code, response_data
