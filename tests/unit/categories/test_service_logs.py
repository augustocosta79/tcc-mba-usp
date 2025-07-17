from unittest.mock import MagicMock
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