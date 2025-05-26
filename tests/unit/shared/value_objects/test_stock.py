from apps.shared.value_objects.stock import Stock
import pytest

class TestStock:
    def test_should_create_stock_with_valid_data(self):
        value = 5
        stock = Stock(value)

        assert isinstance(stock, Stock)
        assert stock.value == value

    def test_should_create_stock_with_value_zero(self):
        value = 0
        stock = Stock(value)

        assert isinstance(stock, Stock)
        assert stock.value == value

    def test_should_sum_two_stocks(self):
        value1 = 2
        value2 = 3

        stock1 = Stock(value1)
        stock2 = Stock(value2)

        result = stock1 + stock2

        assert result == value1 + value2
    
    
    def test_should_subtract_two_stocks(self):
        value1 = 2
        value2 = 3

        stock1 = Stock(value1)
        stock2 = Stock(value2)

        result = stock1 - stock2

        assert result == value1 - value2

    def test_should_raise_value_error_for_values_under_zero(self):
        value = -1
        
        with pytest.raises(ValueError) as exc:
            stock = Stock(value)

        assert "value must be greater or equal zero" in str(exc.value)

    def test_should_raise_value_error_for_not_int_values(self):
        value = "1"
        
        with pytest.raises(ValueError) as exc:
            stock = Stock(value)

        assert "must be an integer number" in str(exc.value)

