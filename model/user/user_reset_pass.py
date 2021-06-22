from model.models import Model


class UserResetPass(Model):
    _end_point = "/user/reset_pass/"

    def __init__(self, email=None, password=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if kwargs:
            self.data = {"email": email, "password": password}
            self.data.update(kwargs)
        elif email and password:
            self.query_param = {"email": email, "password": password}
        elif email:
            self.query_param = {"email": email}
