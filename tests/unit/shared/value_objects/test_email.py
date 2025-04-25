from apps.shared.value_objects.email import Email
import pytest

class TestEmail:
    def test_should_create_email_with_valid_string_format(self):
        formatted_string = "amcneto@hotmail.com"
        email = Email(formatted_string)

        assert isinstance(email, Email)
        assert email.value == formatted_string

    def test_should_raise_error_for_invalid_string_format(self):
        not_email_string_format = "augusto"

        with pytest.raises(ValueError) as exc_info:
            Email(not_email_string_format)

        assert "email válido" in str(exc_info).lower()


    def test_should_strip_email_string(self):
        formatted_string_with_extra_spaces = "  amcneto@hotmail.com "
        email = Email(formatted_string_with_extra_spaces)

        assert isinstance(email, Email)
        assert email.value == formatted_string_with_extra_spaces.strip()