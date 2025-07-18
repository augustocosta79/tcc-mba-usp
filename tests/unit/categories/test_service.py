from datetime import datetime
from uuid import UUID, uuid4
from apps.categories.service import CategoryService
from unittest.mock  import MagicMock
from apps.shared.value_objects import Name, Description
from apps.categories.entity import Category
from apps.shared.exceptions import NotFoundError
from apps.categories.schema import CategoryUpdateSchema
import pytest

def assert_is_equal(saved_category, category):
    assert isinstance(saved_category, Category)
    assert isinstance(saved_category.name, Name)
    assert saved_category.name.value == category.name.value
    assert isinstance(saved_category.description, Description)
    assert saved_category.description.text == category.description.text
    assert isinstance(saved_category.id, UUID)
    assert saved_category.created_at is not None
    assert saved_category.updated_at is not None

@pytest.fixture
def category():
    name = Name("Category")
    description = Description("Category description")
    category = Category(name, description, uuid4(), datetime.now(), datetime.now())

    return category


@pytest.fixture
def service_and_repository():
    repository = MagicMock()
    logger = MagicMock()
    service = CategoryService(repository, logger)

    return service, repository

class TestCategoryService:
    def test_should_create_category_successfully(self, category, service_and_repository):
        service, mock_repository = service_and_repository
        mock_repository.save.return_value = category

        saved_category = service.create_category(category.name.value, category.description.text)

        mock_repository.save.assert_called_once()
        assert_is_equal(saved_category, category)

        

    def test_should_list_categories_successfully(self, category, service_and_repository):
        service, mock_repository = service_and_repository

        mock_repository.list_categories.return_value = [category]
        categories = service.list_categories()

        assert isinstance(categories, list)
        assert len(categories) == 1
        assert_is_equal(categories[0], category)

    def test_should_get_category_by_id_successfully(self, category, service_and_repository):
        service, mock_repository = service_and_repository
        mock_repository.get_category_by_id.return_value = category
        retrieved_category = service.get_category_by_id(category.id)

        mock_repository.get_category_by_id.assert_called_once_with(category.id)
        assert_is_equal(retrieved_category, category)
    
    def test_should_fail_get_category_with_invalid_id(self, category, service_and_repository):
        service, mock_repository = service_and_repository
        mock_repository.get_category_by_id.return_value = None
        
        with pytest.raises(NotFoundError) as exc:
            service.get_category_by_id("invalid id")
        assert "Category not found" in str(exc)

    def test_should_update_category_successfully(self, category, service_and_repository):
        service, mock_repository = service_and_repository
        mock_category = MagicMock()
        payload = CategoryUpdateSchema(
            name="new name",
            description="new description"
        )
        mock_repository.get_category_by_id.return_value = mock_category

        service.update_category(mock_category.id, payload)
        
        mock_repository.get_category_by_id.assert_called_once_with(mock_category.id)
        mock_category.rename.assert_called_once_with(payload.name)
        mock_category.update_description.assert_called_once_with(payload.description)
        mock_repository.update_category.assert_called_once_with(mock_category)
    
    def test_should_fail_update_category_invalid_id(self, category, service_and_repository):
        service, mock_repository = service_and_repository
        payload = CategoryUpdateSchema(
            name="new name",
            description="new description"
        )
        mock_repository.get_category_by_id.return_value = None

        with pytest.raises(NotFoundError) as exc:
            service.update_category("invalid id", payload)
        assert "Category not found" in str(exc)