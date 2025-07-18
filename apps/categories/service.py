from uuid import UUID
from apps.categories.entity import Category
from apps.categories.repository_interface import CategoryRepositoryInterface
import logging
from apps.shared.value_objects import Name, Description
from apps.shared.exceptions import NotFoundError
from apps.categories.schema import CategoryUpdateSchema

class CategoryService:
    def __init__(self, repository: CategoryRepositoryInterface, logger: logging.Logger):
        self.repository = repository
        self.logger = logger

    def create_category(self, str_name: str, str_descriptiom: str) -> Category:
        name = Name(str_name)
        description = Description(str_descriptiom)
        category = Category(name, description)
        saved_category = self.repository.save(category)
        self.logger.info(f"Category successfully created: Name {saved_category.name.value} - ID {saved_category.id}")
        return saved_category
    
    def list_categories(self) -> list[Category]:
        return self.repository.list_categories()
    
    def get_category_by_id(self, category_id: UUID):
        if not (category:=self.repository.get_category_by_id(category_id)):
            raise NotFoundError(f"Category not found - ID {category_id}")
        return category
    
    def update_category(self, category_id:UUID, payload:CategoryUpdateSchema) -> Category:
        if not (category:=self.repository.get_category_by_id(category_id)):
            self.logger.warning(f"Category not found - ID {category_id}")
            raise NotFoundError(f"Category not found - ID {category_id}")
        
        operations = {
            "name": category.rename,
            "description": category.update_description
        }

        for attr, value in payload.dict(exclude_unset=True).items():
            operations[attr](value)

        updated_category = self.repository.update_category(category)
        self.logger.info(f"Category successfully updated - New name {updated_category.name.value}, Id {updated_category.id}")
        return updated_category