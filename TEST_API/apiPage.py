import requests

class apiPage:

    def __init__(self, base_url: str) -> None:
        self.base_url = base_url

    def get_json(self, url: str):
        resp = requests.get(self.base_url + url)
        return resp.json()

    def get_obj(self, url: str):
        resp = requests.get(self.base_url + url)
        return resp

    def post_obj(self, json: list[str]):
        resp = requests.post(self.base_url, json= json)
        return resp
