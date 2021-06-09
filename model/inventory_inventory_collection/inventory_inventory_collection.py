from model.api import Api
from model.models import Model


class InventoryInventoryCollection(Model):
    _end_point = "/inventory_inventory_collection/"

    def __init__(self, *args, inventory_collection_id=None, **kwargs):
        super().__init__(*args, **kwargs)
        if args:
            self.data = args
        elif kwargs:
            self.data = kwargs
            self.data.update({"inventory_collection_id": inventory_collection_id})
        if inventory_collection_id:
            self.query_param = {"inventory_collection_id": inventory_collection_id}


# class InventoryInventoryCollection:
#     _end_point = "/inventory_inventory_collection/"
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
#         return response_code, response_data
