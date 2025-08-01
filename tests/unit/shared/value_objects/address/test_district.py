from apps.shared.value_objects.address.district import District
import pytest

class TestDistrict:
    def test_district_creation(self):
        district = District("Leblon")
        assert district.value == "Leblon"

    def test_district_validation(self):
        with pytest.raises(ValueError):
            District("")

        with pytest.raises(ValueError):
            District("  ")

        with pytest.raises(ValueError):
            District("L")

        with pytest.raises(ValueError):
            District("L" * 201)
