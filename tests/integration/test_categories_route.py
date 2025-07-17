import json
import pytest
from tests.utils.timed_client import TimedClient

@pytest.fixture
def timed_client(client):
    return TimedClient(client)

@pytest.mark.django_db
class TestCreateCategory:
    def test_should_create_category(self, timed_client):
        url = "/api/categories"

        payload = {
            "name": "Category",
            "description": "cat description"
        }

        response = timed_client.post(
            url, data=json.dumps(payload), content_type="application/json"
        )
        assert response.status_code == 201

        body = response.json()

        assert body["id"] is not None
        assert body["name"] == payload["name"]
        assert body["description"] == payload["description"]
        assert body["created_at"] is not None
        assert body["updated_at"] is not None