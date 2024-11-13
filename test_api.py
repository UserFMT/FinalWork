import pytest

from params import params
from AviaPage import ApiPage

headers = {
    "Authorization" : f"{params.Authorization}",
    "path":f"{params.URL_API}",
    "Content-Type": "application/json"
}


user = ApiPage.init_user(headers)

