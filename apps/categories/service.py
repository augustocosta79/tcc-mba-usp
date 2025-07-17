from apps.categories.entity import Category
from apps.categories.repository_interface import CategoryRepositoryInterface
import logging
from apps.shared.value_objects import Name, Description

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