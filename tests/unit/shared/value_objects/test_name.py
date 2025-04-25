from apps.shared.value_objects.name import Name
import pytest

class TestName:
    def test_should_create_name_with_valid_string(self):
        string = "Augusto"
        name = Name(string)

        assert isinstance(name, Name)
        assert name.value == string

    def test_should_strip_spaces(self):
        string = "  Augusto  "
        name = Name(string)

        assert isinstance(name, Name)
        assert name.value == string.strip()

    def test_should_raise_error_for_empty_names(self):
        with pytest.raises(ValueError) as exc_info:
            Name("")
        assert "obrigatório" in str(exc_info.value).lower()