from model.models import Model


class Truck(Model):
    _end_point = "/truck/"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
