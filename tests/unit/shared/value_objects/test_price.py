from apps.shared.value_objects.price import Price
from decimal import Decimal


class TestPrice:
    def test_should_create_price_with_valid_string_value(self):
        value = "1.99"
        price = Price(value)
        price2 = Price("1.00")

        assert price.value == Decimal(value)
        assert price + price2 == Decimal("2.99")
        assert str(price) == f"R${price.value}"
    
    
    def test_should_create_price_with_valid_number_value(self):
        value = 1.99
        price = Price(value)
        price2 = Price(1)

        assert price.value == Decimal(str(value))
        assert price + price2 == Decimal("2.99")
        assert str(price) == f"R${price.value}"

    def test_should_sum_two_prices(self):
        value1 = 2
        value2 = 3

        price1 = Price(value1)
        price2 = Price(value2)

        result = price1 + price2

        assert result == value1 + value2
    
    
    def test_should_subtract_two_prices(self):
        value1 = 2
        value2 = 3

        price1 = Price(value1)
        price2 = Price(value2)

        result = price1 - price2

        assert result == value1 - value2