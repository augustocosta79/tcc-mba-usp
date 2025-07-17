from datetime import datetime
from uuid import UUID, uuid4
from apps.categories.repository import CategoryRepository
from apps.shared.value_objects import Name, Description
from apps.categories.entity import Category
import pytest

repository = CategoryRepository()

@pytest.fixture
def create_category():
    name = Name("name")
    description = Description("description")
    category = Category(name, description)
    saved_category = repository.save(category)
    
    return category, saved_category

@pytest.mark.django_db
class TestCategoryRepository:
    def test_should_save_category_successfully(self, create_category):
        category, saved_category = create_category

        assert isinstance(saved_category, Category)
        assert isinstance(saved_category.name, Name)
        assert isinstance(saved_category.description, Description)
        assert saved_category.name.value == category.name.value
        assert saved_category.description.text == category.description.text
        assert saved_category.id is not None
        assert isinstance(saved_category.id, UUID)
        assert saved_category.created_at is not None
        assert isinstance(saved_category.created_at, datetime)
        assert saved_category.updated_at is not None
        assert isinstance(saved_category.updated_at, datetime)