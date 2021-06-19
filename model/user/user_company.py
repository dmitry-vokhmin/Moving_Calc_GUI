from model.models import Model


class UserCompany(Model):
    _end_point = "/user/company/"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
