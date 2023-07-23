import logging
from http import HTTPStatus

import pytest
import requests

from tests.functional.utils.constants import UserData
from tests.functional.utils.routes import AUTH_URL_LOGIN, AUTH_URL_SIGN_UP


@pytest.fixture(scope="session", autouse=True)
async def create_user_default():
    requests.post('http://auth:8000/api/v1/auth/sign_up', headers={"X-Request-Id": "1"}, json={
        'login': UserData.LOGIN,
        'password': UserData.PASSWORD,
        'name': UserData.NAME
    })
    logging.info("User successfully created")


@pytest.fixture(scope="session")
async def user_access_token():
    resp = requests.post(
        AUTH_URL_LOGIN,
        headers={"X-Request-Id": "1"},
        json={
            'login': UserData.LOGIN,
            'password': UserData.PASSWORD
        }
    )
    if resp.status_code != HTTPStatus.OK:
        raise Exception(resp.text)

    resp_data = resp.json()

    return resp_data['access_token']