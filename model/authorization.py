from config import TOKEN_FILE
from model import api


class AuthorizationError(Exception):
    pass


class Authorization:
    _token = None
    _end_point = "/authorization/"
    __instance = None

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls, *args, **kwargs)
        return cls.__instance

    def check_authorization(self):
        if TOKEN_FILE.exists():
            Authorization._token = TOKEN_FILE.read_text()
        if not Authorization._token:
            raise AuthorizationError("Not Authorized")
        self.check_token()

    @classmethod
    def delete_token(cls):
        if TOKEN_FILE.exists():
            TOKEN_FILE.write_text("")
        cls._token = None

    @classmethod
    def post(cls, user):
        new_api = api.Api()
        cls.to_json = user.to_json
        response_code, response_data = new_api.post(cls)
        if response_code > 399:
            raise AuthorizationError("Not Authorized")
        cls._token = response_data["access_token"]
        return response_data

    def check_token(self):
        # TODO: проверить что токен живой
        pass
