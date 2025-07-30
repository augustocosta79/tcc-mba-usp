class District:
    def __init__(self, value: str):
        self.value = value
        self._validate()

    def _validate(self):
        if not isinstance(self.value, str):
            raise ValueError("District must be a string")
        if not self.value.strip():
            raise ValueError("District cannot be empty")
        if len(self.value) > 200:
            raise ValueError("District cannot exceed 200 characters")
        if len(self.value) < 3:
            raise ValueError("District must be at least 3 characters long")
        
    def __str__(self):
        return self.value

    def __eq__(self, other):
        return isinstance(other, District) and self.value == other.value

    def __hash__(self):
        return hash(self.value)