from model.models import Model


class UserPrivilege(Model):
    _end_point = "/user_privilege/"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
