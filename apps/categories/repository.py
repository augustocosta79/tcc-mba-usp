from apps.categories.entity import Category
from apps.categories.repository_interface import CategoryRepositoryInterface
from apps.categories.models import CategoryModel
from apps.shared.value_objects import Name, Description

class CategoryRepository(CategoryRepositoryInterface):
    def save(self, category: Category) -> Category:
        category_data = CategoryModel.objects.create(
            id=category.id,
            name=category.name.value,
            description=category.description.text,
            created_at=category.created_at,
            updated_at=category.updated_at
        )
        return Category(
            name=Name(category_data.name),
            description=Description(category_data.description),
            id=category_data.id,
            created_at=category_data.created_at,
            updated_at=category_data.updated_at,
        )