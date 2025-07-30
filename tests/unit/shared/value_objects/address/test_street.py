from apps.shared.value_objects.address.street import Street

class TestStreet:
    def test_street_initialization(self):
        street = Street("123 Main St")
        assert street.value == "123 Main St"

    def test_street_equality(self):
        street1 = Street("123 Main St")
        street2 = Street("123 Main St")
        assert street1 == street2

    def test_street_inequality(self):
        street1 = Street("123 Main St")
        street2 = Street("456 Elm St")
        assert street1 != street2