from model.models import Model


class ZipCode(Model):
    _end_point = "/zip_code/"

    def __init__(self, zip_code, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if zip_code:
            self.query_param = {"zip_code": zip_code}
