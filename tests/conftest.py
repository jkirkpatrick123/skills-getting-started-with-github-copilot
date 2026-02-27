import copy
import pytest
from fastapi.testclient import TestClient
from src import app as app_module

original = copy.deepcopy(app_module.activities)

@pytest.fixture
def client():
    with TestClient(app_module.app) as c:
        yield c

@pytest.fixture(autouse=True)
def reset_activities():
    app_module.activities = copy.deepcopy(original)
    yield
