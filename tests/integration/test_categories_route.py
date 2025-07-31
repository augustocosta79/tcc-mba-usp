import json
from uuid import UUID, uuid4
from tests.utils.assertions import assert_has_valid_id, assert_has_valid_timestamps
import pytest
from tests.utils.timed_client import TimedClient
from apps.categories.service import CategoryService
from apps.categories.repository import CategoryRepository
from utils.logger import configure_logger

@pytest.fixture
def timed_client(client):
    return TimedClient(client)

@pytest.fixture
def test_category():
    repository = CategoryRepository()
    logger = configure_logger(__name__)
    service= CategoryService(repository, logger)
    category = service.create_category("name", "description")
    return category

@pytest.mark.django_db
class TestCreateCategory:
    def test_should_create_category_successfully(self, timed_client):
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

        assert_has_valid_id(body)
        assert body["name"] == payload["name"]
        assert body["description"] == payload["description"]        
        assert_has_valid_timestamps(body)


@pytest.mark.django_db
class TestListCategories:
    def test_should_list_categories_successfully(self, timed_client, test_category):
        url = "/api/categories"
        response = timed_client.get(url)
        assert response.status_code == 200

        body = response.json()

        assert isinstance(body, list)
        assert_has_valid_id(body[0])
        assert body[0]["name"] == test_category.name.value
        assert body[0]["description"] == test_category.description.value
        assert_has_valid_timestamps(body[0])


@pytest.mark.django_db
class TestGetCategoryById:
    def test_should_get_category_by_id_successfully(self, timed_client, test_category):
        url = f"/api/categories/{test_category.id}"
        response = timed_client.get(url)
        assert response.status_code == 200

        body = response.json()

        assert_has_valid_id(body)
        assert body["name"] == test_category.name.value
        assert body["description"] == test_category.description.value
        assert_has_valid_timestamps(body)


@pytest.mark.django_db
class TestUpdateCategoryData:
    def test_should_get_category_by_id_successfully(self, timed_client, test_category):
        url = f"/api/categories/{test_category.id}"

        payload = {
            "name": "new name",
            "description": "new description"
        }
        response = timed_client.patch(
            url, data=json.dumps(payload), content_type="application/json"
        )
        assert response.status_code == 200

        body = response.json()

        assert_has_valid_id(body)
        assert UUID(body["id"]) == test_category.id
        assert body["name"] == payload["name"]
        assert body["description"] == payload["description"]
        assert_has_valid_timestamps(body)


@pytest.mark.django_db
class TestDeleteCategory:
    def test_should_delete_category_by_id_successfully(self, timed_client, test_category):
        url = f"/api/categories/{test_category.id}"
        response = timed_client.delete(url)
        assert response.status_code == 204
    
    def test_should_fail_delete_category_invalid_id(self, timed_client, test_category):
        url = f"/api/categories/{uuid4()}"
        response = timed_client.delete(url)
        assert response.status_code == 404