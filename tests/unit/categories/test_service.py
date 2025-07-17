from datetime import datetime
from uuid import UUID, uuid4
from apps.categories.service import CategoryService
from unittest.mock  import MagicMock
from apps.shared.value_objects import Name, Description
from apps.categories.entity import Category
import pytest

@pytest.fixture
def create_category():
    name = Name("Category")
    description = Description("Category description")
    category = Category(name, description, uuid4(), datetime.now(), datetime.now())

    return category, name, description


@pytest.fixture
def create_service():
    repository = MagicMock()
    logger = MagicMock()
    service = CategoryService(repository, logger)

    return service, repository

class TestCategoryService:
    def test_should_create_category_successfully(self, create_category, create_service):
        category, name, description = create_category
        service, mock_repository = create_service
        mock_repository.save.return_value = category

        category = service.create_category(name.value, description.text)

        mock_repository.save.assert_called_once()

        assert isinstance(category.name, Name)
        assert category.name.value == name.value
        assert isinstance(category.description, Description)
        assert category.description.text == description.text
        assert isinstance(category.id, UUID)
        assert category.created_at is not None
        assert category.updated_at is not None