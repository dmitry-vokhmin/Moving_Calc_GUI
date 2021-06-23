from model.models import Model


class Registration(Model):
    _end_point = "/registration/"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
