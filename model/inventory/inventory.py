from model.models import Model


class Inventory(Model):
    _end_point = "/inventory/"

    def __init__(self, room_collection_id=None, category_id=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if room_collection_id and category_id:
            self.query_param = {"room_collection_id": room_collection_id, "category_id": category_id}
        elif room_collection_id:
            self.query_param = {"room_collection_id": room_collection_id}
