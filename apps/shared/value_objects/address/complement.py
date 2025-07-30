class Complement:
    def __init__(self, value: str):
        self.value = value
        self._validate()

    def _validate(self):
        if not len(self.value.strip()) > 0:
            raise ValueError("Complement can not be empty.")
    
    def __str__(self):
        return self.value
    
    def __eq__(self, other):
        return self.value == other.value and isinstance(other, Complement)
    
    def __hash__(self):
        return hash(self.value)