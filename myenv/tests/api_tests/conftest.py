import pytest
import requests


@pytest.fixture
def base_url():
    return "https://jsonplaceholder.typicode.com/"


@pytest.fixture
def api_client(base_url):
    return requests.Session()
