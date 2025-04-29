import pytest
from apps.shared.value_objects.password import Password

class TestPassword:
    def test_should_create_password_with_valid_format(self):
        password = Password("Abc@1234")
        assert isinstance(password, Password)
        assert password.hash is not None
        assert password.verify("Abc@1234")

    def test_should_raise_error_if_less_than_8_characters(self):
        with pytest.raises(ValueError) as exc:
            Password("Ab1@a")
        assert "8 caracteres" in str(exc.value).lower()

    def test_should_raise_error_if_no_uppercase_letter(self):
        with pytest.raises(ValueError) as exc:
            Password("abc@1234")
        assert "maiúscula" in str(exc.value).lower()

    def test_should_raise_error_if_no_lowercase_letter(self):
        with pytest.raises(ValueError) as exc:
            Password("ABC@1234")
        assert "minúscula" in str(exc.value).lower()

    def test_should_raise_error_if_no_number(self):
        with pytest.raises(ValueError) as exc:
            Password("Abc@defg")
        assert "número" in str(exc.value).lower()

    def test_should_raise_error_if_no_special_character(self):
        with pytest.raises(ValueError) as exc:
            Password("Abc12345")
        assert "símbolo" in str(exc.value).lower()

    def test_should_compare_passwords_by_hash(self):
        pwd1 = Password("Abc@1234")
        pwd2 = Password("Abc@1234")
        assert pwd1 != pwd2  # pois o hash inclui salt

        # Mas ambos devem verificar a mesma senha com verify
        assert pwd1.verify("Abc@1234")
        assert pwd2.verify("Abc@1234")
