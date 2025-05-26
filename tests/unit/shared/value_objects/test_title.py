from apps.shared.value_objects import Title
import pytest

class TestTitle:
    def test_should_create_title_with_valid_data(self):
        title_string = "great SEO title"
        title = Title(title_string)

        assert isinstance(title, Title)
        assert title.text == title_string


    def test_should_raise_value_error_for_less_than_two_char_string(self):
        title_string = "a"

        with pytest.raises(ValueError) as exc:
            title = Title(title_string)
        
        assert "more than two characters" in str(exc.value)

    def test_should_raise_value_error_for_not_string_text(self):
        with pytest.raises(ValueError) as exc:
            Title(123)

        assert "must be a string" in str(exc.value)

