from model.models import Model


class Calculator(Model):
    _end_point = "/calculate/"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
