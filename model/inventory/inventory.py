from model.api import Api


class Inventory:
    _end_point = "/inventory/"

    def __init__(self, room_collection_id=None, inventory_collection_id=None, *args, **kwargs):
        if room_collection_id:
            self._end_point = f"/inventory/?room_collection_id={room_collection_id}"
        elif inventory_collection_id:
            self._end_point = f"/inventory/?inventory_collection_id={inventory_collection_id}"
        self.args = args
        self.data = kwargs

    @property
    def to_json(self):
        return self.data

    def get(self):
        api = Api()
        response_code, response_data = api.get(self)
        return response_code, response_data

    def post(self):
        api = Api()
        response_code, response_data = api.post(self)
        return response_code, response_data
