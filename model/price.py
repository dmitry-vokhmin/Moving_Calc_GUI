from model.models import Model


class Price(Model):
    _end_point = "/price/"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.data = args
