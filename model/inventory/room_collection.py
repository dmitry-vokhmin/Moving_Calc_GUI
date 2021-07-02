from model.models import Model


class RoomCollection(Model):
    _end_point = "/room_collection/"

    def __init__(self, inventory_id=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if inventory_id:
            self.query_param = {"inventory_id": inventory_id}
