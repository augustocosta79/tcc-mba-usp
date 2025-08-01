from apps.shared.value_objects import City
import pytest

class TestCity:
    def test_should_create_city_with_string_value(self):
        city = City("São Paulo")
        assert city.value == "São Paulo"

    def test_should_successfully_compare_city_equality(self):
        city1 = City("São Paulo")
        city2 = City("São Paulo")
        assert city1 == city2

    def ttest_should_successfully_compare_city_inequality(self):
        city1 = City("São Paulo")
        city2 = City("Rio de Janeiro")
        assert city1 != city2

    def test_empty_string_should_raise_value_error(self):
        with pytest.raises(ValueError):
            City("")