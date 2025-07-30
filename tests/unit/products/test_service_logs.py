from unittest.mock import MagicMock
from uuid import uuid4

from apps.products.schema import ProductActivationSchema, ProductUpdateSchema
import pytest
from apps.products.service import ProductService
from apps.shared.exceptions import NotFoundError
from apps.categories.entity import Category

mock_product = MagicMock()
mock_user = MagicMock()
mock_user_service = MagicMock()

@pytest.fixture
def create_service():
    mock_repository = MagicMock()
    mock_logger = MagicMock()
    mock_category_service = MagicMock()
    service = ProductService(mock_repository, mock_logger, mock_category_service, mock_user_service)

    return service, mock_repository, mock_logger

@pytest.fixture
def product_args() -> list:
    title = "title"
    description = "description"
    price = "1.99"
    stock = 5
    owner_id = mock_user.id
    cat_name = "Category"
    cat_desc = "Cat desc"
    test_category = Category(name=cat_name, description=cat_desc)
    categories_ids = [ test_category.id ]

    return [title, description, price, stock, owner_id, categories_ids]

class TestProductsLogs:
    def test_should_log_product_creation_successfully(self, product_args: list, create_service):
        args = product_args
        service, mock_repository, mock_logger = create_service
        mock_user_service.get_user_by_id.return_value = mock_user
        service.create_product(*args)
        mock_logger.info.assert_called_once()
        assert "Product successfully created" in mock_logger.info.call_args[0][0]

    def test_should_log_product_update_successfully(self, create_service):
        service, mock_repository, mock_logger = create_service
        mock_repository.get_product_by_id.return_value = mock_product
        mock_repository.update_product.return_value = mock_product

        schema = ProductUpdateSchema(title="Teste")
        service.update_product(mock_product.id, schema)

        mock_logger.info.assert_called_once()
        assert "Product successfully updated" in mock_logger.info.call_args[0][0]

    def test_should_log_product_update_not_found_failure_successfully(self, create_service):
        service, mock_repository, mock_logger = create_service
        mock_repository.get_product_by_id.return_value = None
        schema = ProductUpdateSchema(title="Teste")

        with pytest.raises(NotFoundError):
            service.update_product(mock_product.id, schema)

        mock_logger.warning.assert_called_once()
        assert "Product not found" in mock_logger.warning.call_args[0][0]


    def test_should_log_product_activation_successfully(self, create_service):
        service, mock_repository, mock_logger = create_service
        payload = ProductActivationSchema(status=True)
        mock_repository.get_product_by_id.return_value = mock_product

        service.product_activation(mock_product.id, payload)

        mock_logger.info.assert_called_once()
        assert "activated successfully" in mock_logger.info.call_args[0][0]

    def test_should_log_product_deactivation_successfully(self, create_service):
        service, mock_repository, mock_logger = create_service
        payload = ProductActivationSchema(status=False)
        mock_repository.get_product_by_id.return_value = mock_product

        service.product_activation(mock_product.id, payload)

        mock_logger.info.assert_called_once()
        assert "deactivated successfully" in mock_logger.info.call_args[0][0]


    def test_should_log_not_found_product_activation_successfully(self, create_service):
        service, mock_repository, mock_logger = create_service
        payload = ProductActivationSchema(status=True)
        mock_repository.get_product_by_id.return_value = None

        with pytest.raises(NotFoundError):
            service.product_activation(mock_product.id, payload)

        mock_logger.warning.assert_called_once()
        assert "Product not found" in mock_logger.warning.call_args[0][0]

    def test_should_log_product_deletion_successfully(self, create_service):
        service, mock_repository, mock_logger = create_service
        mock_repository.get_product_by_id.return_value = mock_product
        service.delete_product(mock_product.id)

        mock_logger.info.assert_called_once()
        assert "Product successfully deleted" in mock_logger.info.call_args[0][0]
    
    def test_should_log_not_found_product_deletion_failure_successfully(self, create_service):
        service, mock_repository, mock_logger = create_service
        mock_repository.get_product_by_id.return_value = None

        with pytest.raises(NotFoundError):
            service.delete_product(mock_product.id)

        mock_logger.warning.assert_called_once()
        assert "Not found Product" in mock_logger.warning.call_args[0][0]