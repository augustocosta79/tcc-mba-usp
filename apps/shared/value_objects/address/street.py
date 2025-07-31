from apps.shared.value_objects.base import StringVO

class Street(StringVO):
    def _validate(self):
        if not isinstance(self.value, str):
            raise ValueError("Street must be a string")
        if not self.value.strip():
            raise ValueError("Street cannot be empty")
        if len(self.value.strip()) < 2:
            raise ValueError("Street must have more than one character")
        if not any(char.isalpha() for char in self.value):
            raise ValueError("Street must contain letters")
        if self.value.lower() in ["sem nome", "s/n", ""]:
            raise ValueError("Invalid street name")
