from uuid import UUID
from apps.categories.entity import Category
from apps.categories.repository_interface import CategoryRepositoryInterface
from apps.categories.models import CategoryModel
from apps.shared.value_objects import Name, Description

class CategoryRepository(CategoryRepositoryInterface):
    def save(self, category: Category) -> Category:
        category_data = CategoryModel.objects.create(
            id=category.id,
            name=category.name.value,
            description=category.description.value,
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
    
    def list_categories(self) -> list[Category]:
        categories_data = CategoryModel.objects.all()
        return [
            Category(
            name=Name(category_data.name),
            description=Description(category_data.description),
            id=category_data.id,
            created_at=category_data.created_at,
            updated_at=category_data.updated_at,
            )
            for category_data in categories_data
        ]
    
    def get_category_by_id(self, category_id:UUID):
        if not (category_data:=CategoryModel.objects.filter(id=category_id).first()):
            return None
        return Category(
            name=Name(category_data.name),
            description=Description(category_data.description),
            id=category_data.id,
            created_at=category_data.created_at,
            updated_at=category_data.updated_at,
            )
    
    def update_category(self, category: Category) -> Category:
        if not (category_data:=CategoryModel.objects.filter(id=category.id).first()):
            return None
        category_data.name = category.name.value
        category_data.description = category.description.value
        category_data.save()
        return Category(
            name=Name(category_data.name),
            description=Description(category_data.description),
            id=category_data.id,
            created_at=category_data.created_at,
            updated_at=category_data.updated_at,
        )
    
    def delete_category(self, category_id:UUID):
        if not (category:=CategoryModel.objects.filter(id=category_id).first()):
            return None
        category.delete()