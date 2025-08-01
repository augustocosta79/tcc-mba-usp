from apps.shared.value_objects import StateCode
import pytest

class TestStateCode:
    def test_should_create_state_code_with_valid_string(self):
        state_code = StateCode("SP")
        assert state_code.value == "SP"

    def test_should_create_state_code_with_three_letters(self):
        state_code = StateCode("SPO")
        assert state_code.value == "SPO"

    def test_should_raise_value_error_for_invalid_length(self):
        with pytest.raises(ValueError):
            StateCode("S")

        with pytest.raises(ValueError):
            StateCode("SPQW")

    def test_should_raise_value_error_for_non_uppercase_letters(self):
        with pytest.raises(ValueError):
            StateCode("sp")

        with pytest.raises(ValueError):
            StateCode("SpO")