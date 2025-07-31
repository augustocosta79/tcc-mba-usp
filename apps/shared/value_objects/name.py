from apps.shared.value_objects.base import StringVO

class Name(StringVO):
    def __init__(self, value: str):
        super().__init__(value.strip())

    def _validate(self):
        if not self.value:
            raise ValueError("O nome é obrigatório.")
        
        if any(char.isdigit() for char in self.value):
            raise ValueError("O nome não pode conter números")
