from datetime import datetime
from uuid import UUID, uuid4
from apps.categories.repository import CategoryRepository
from apps.shared.value_objects import Name, Description
from apps.categories.entity import Category
import pytest

repository = CategoryRepository()

def assert_is_equal(saved_category, category):
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

@pytest.fixture
def category_and_saved_category():
    name = Name("name")
    description = Description("description")
    category = Category(name, description)
    saved_category = repository.save(category)
    
    return category, saved_category

@pytest.mark.django_db
class TestCategoryRepository:
    def test_should_save_category_successfully(self, category_and_saved_category):
        category, saved_category = category_and_saved_category
        assert_is_equal(saved_category, category)
        

    def test_should_retrive_categories_list(self, category_and_saved_category):
        category, saved_category = category_and_saved_category

        categories = repository.list_categories()
        assert categories[0] is not None

        retrieved_category = categories[0]
        assert_is_equal(retrieved_category, saved_category)
        assert_is_equal(retrieved_category, category)

    def test_should_get_category_by_id_successfully(self, category_and_saved_category):
        category, saved_category = category_and_saved_category
        retrieved_category = repository.get_category_by_id(saved_category.id)
        assert_is_equal(retrieved_category, saved_category)
        assert_is_equal(retrieved_category, category)