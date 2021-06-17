from model.models import Model


class Company(Model):
    _end_point = "/company/"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
