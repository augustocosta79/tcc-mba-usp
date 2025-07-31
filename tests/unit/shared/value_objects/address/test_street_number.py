from apps.shared.value_objects import StreetNumber
import pytest

class TestStreetNumber:
    def test_street_number_initialization(self):
        street_number = StreetNumber("123")
        assert street_number.value == "123"

    def test_street_number_validation(self):
        with pytest.raises(ValueError):
            StreetNumber("abc")

    def test_street_number_equality(self):
        street_number1 = StreetNumber("123")
        street_number2 = StreetNumber("123")
        assert street_number1 == street_number2

    def test_street_number_inequality(self):
        street_number1 = StreetNumber("123")
        street_number2 = StreetNumber("456")
        assert street_number1 != street_number2
