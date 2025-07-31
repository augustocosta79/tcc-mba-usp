from apps.shared.value_objects.base import StringVO

class StreetNumber(StringVO):    
    def _validate(self):
        if not isinstance(self.value, str):
            raise ValueError("Street number must be a string")
        if not self.value.strip():
            raise ValueError("Street number cannot be empty")
        if not self.value.isdigit():
            raise ValueError("Street number must contain only digits")
        if int(self.value) < 0:
            raise ValueError("Street value cannot be negative")
