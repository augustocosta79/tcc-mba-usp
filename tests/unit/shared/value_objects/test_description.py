from apps.shared.value_objects import Description
import pytest

class TestDescription:
    def test_should_create_description_with_valid_string(self):
        description_string = "some awesome descrition"
        description = Description(description_string)

        assert isinstance(description, Description)
        assert description.value == description_string

    def test_should_raise_value_error_for_under_five_char_string(self):
        with pytest.raises(ValueError) as exc:
            Description("hi!")

        assert "must have at least five characters" in str(exc.value)

    def test_should_raise_value_error_for_white_space_strings(self):
        with pytest.raises(ValueError) as exc:
            Description("      ")

        assert "must not be empty or just white spaces" in str(exc.value)


    def test_should_raise_value_error_for_not_string_values(self):
        with pytest.raises(ValueError) as exc:
            Description(5)

        assert "text must be a string" in str(exc.value)