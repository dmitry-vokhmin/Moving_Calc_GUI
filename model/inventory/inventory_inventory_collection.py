from model.models import Model


class InventoryInventoryCollection(Model):
    _end_point = "/inventory_inventory_collection/"

    def __init__(self, *args, inventory_collection_id=None, move_size_id=None, **kwargs):
        super().__init__(*args, **kwargs)
        if args:
            self.data = args
        elif kwargs:
            self.data = kwargs
            self.data.update({"inventory_collection_id": inventory_collection_id})
        if inventory_collection_id:
            self.query_param = {"inventory_collection_id": inventory_collection_id}
        elif move_size_id:
            self.query_param = {"move_size_id": move_size_id}
