from model.models import Model


class TruckType(Model):
    _end_point = "/truck_type/"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
