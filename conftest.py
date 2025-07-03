import pytest
import os
import json
from base64 import b64encode
from ninja.testing import TestClient
from ninja import NinjaAPI
from django.core.management import call_command
from ninja_knox.router import router
import ninja_knox.views

os.environ['NINJA_SKIP_REGISTRY'] = "True"

@pytest.fixture(scope='session')
def api():
    return NinjaAPI()

@pytest.fixture(scope='session')
def client(api: NinjaAPI):
    api.add_router('', router)
    print(api.urls)
    return TestClient(api) 

@pytest.fixture(scope='module')
def get_basic_auth_header():
    def _get_basic_auth_header(username: str, password: str):
        token = b64encode(f"{username}:{password}".encode('utf-8')).decode("ascii")
        return f'Basic {token}'
    return _get_basic_auth_header

@pytest.fixture
def get_test_user(django_db_blocker, django_user_model):
    def _get_test_user(id):
        with django_db_blocker.unblock():
            return django_user_model.objects.get(pk=id)
    return _get_test_user

@pytest.fixture(scope='session')
def django_db_setup(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        call_command('loaddata', 'test_data.yaml')
