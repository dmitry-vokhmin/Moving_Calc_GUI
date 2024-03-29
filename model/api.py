from urllib.parse import urljoin
import requests
from model import authorization


class Api:
    _domain = "https://moving-calculator.herokuapp.com/"
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
        if model.query_param:
            response = requests.get(url,
                                    params=model.query_param,
                                    headers={"Authorization": f"Bearer {authorization.Authorization()._token}"}
                                    )
        else:
            response = requests.get(url, headers={"Authorization": f"Bearer {authorization.Authorization()._token}"})
        return response.status_code, response.json()

    def delete(self, model):
        url = urljoin(self._domain, model._end_point)
        if model.query_param:
            response = requests.delete(url,
                                       params=model.query_param,
                                       json=model.to_json,
                                       headers={"Authorization": f"Bearer {authorization.Authorization()._token}"}
                                       )
        else:
            response = requests.delete(url,
                                       json=model.to_json,
                                       headers={"Authorization": f"Bearer {authorization.Authorization()._token}"})
        return response.status_code, response.json()
