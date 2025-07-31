from apps.shared.value_objects.base import StringVO


class District(StringVO):
    def _validate(self):
        if not isinstance(self.value, str):
            raise ValueError("District must be a string")
        if not self.value.strip():
            raise ValueError("District cannot be empty")
        if len(self.value) > 200:
            raise ValueError("District cannot exceed 200 characters")
        if len(self.value) < 3:
            raise ValueError("District must be at least 3 characters long")
