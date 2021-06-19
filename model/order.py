from model.models import Model


class Order(Model):
    _end_point = "/order/"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
