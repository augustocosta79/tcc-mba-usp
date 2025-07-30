class StreetNumber:
    def __init__(self, value: str):
        self.value = value
        self._validate()
    
    def _validate(self):
        if not isinstance(self.value, str):
            raise ValueError("Street number must be a string")
        if not self.value.strip():
            raise ValueError("Street number cannot be empty")
        if not self.value.isdigit():
            raise ValueError("Street number must contain only digits")
        if int(self.value) < 0:
            raise ValueError("Street value cannot be negative")
        
    def __str__(self):
        return self.value

    def __eq__(self, other):
        return isinstance(other, StreetNumber) and self.value == other.value

    def __hash__(self):
        return hash(self.value)