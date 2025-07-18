from unittest.mock import MagicMock
from apps.shared.exceptions.exceptions import NotFoundError
from apps.categories.schema import CategoryUpdateSchema
from apps.categories.service import CategoryService
import pytest


mock_category = MagicMock()

@pytest.fixture
def create_service():
    repository = MagicMock()
    logger = MagicMock()
    service = CategoryService(repository, logger)

    return service, repository, logger


class TestCategoryServiceLogs:
    def test_should_log_category_creation_successfully(self, create_service):
        service, mock_repository, mock_logger = create_service
        mock_repository.save_category.return_value = mock_category
        service.create_category("category", "description")

        mock_logger.info.assert_called_once()
        assert "Category successfully created" in mock_logger.info.call_args[0][0]

    def test_should_log_category_update_successfully(self, create_service):
        service, mock_repository, mock_logger = create_service
        mock_repository.get_category_by_id.return_value = mock_category
        mock_repository.save.return_value = mock_category
        payload = CategoryUpdateSchema(
            name="new name",
            description="new description"
        )
        service.update_category(mock_category.id, payload)
        mock_logger.info.assert_called_once()
        assert "Category successfully updated" in mock_logger.info.call_args[0][0]
    
    def test_should_log_category_update_failure_successfully(self, create_service):
        service, mock_repository, mock_logger = create_service
        mock_repository.get_category_by_id.return_value = None
        payload = CategoryUpdateSchema(
            name="new name",
            description="new description"
        )
        with pytest.raises(NotFoundError):
            service.update_category(mock_category.id, payload)
        mock_logger.warning.assert_called_once()
        assert "Category not found" in mock_logger.warning.call_args[0][0]