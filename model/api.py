from urllib.parse import urljoin
import requests
from model.user import authorization


class Api:
    _domain = "http://127.0.0.1:8080/"
    __instance = None

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls, *args, **kwargs)
        return cls.__instance

    def post(self, model):
        url = urljoin(self._domain, model._end_point)
        response = requests.post(url,
                                 json=model.to_json,
                                 headers={"Authorization": f"Bearer {authorization.Authorization()._token}"})
        return response.status_code, response.json()

    def put(self, model):
        url = urljoin(self._domain, model._end_point)
        response = requests.put(url,
                                json=model.to_json,
                                headers={"Authorization": f"Bearer {authorization.Authorization()._token}"})
        return response.status_code, response.json()

    def get(self, model):
        url = urljoin(self._domain, model._end_point)
        response = requests.get(url, headers={"Authorization": f"Bearer {authorization.Authorization()._token}"})
        return response.status_code, response.json()

    def delete(self, model):
        url = urljoin(self._domain, model._end_point)
        response = requests.delete(url,
                                   json=model.to_json,
                                   headers={"Authorization": f"Bearer {authorization.Authorization()._token}"})
        return response.status_code, response.json()
