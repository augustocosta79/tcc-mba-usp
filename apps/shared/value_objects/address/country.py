import re
from apps.shared.value_objects.base import StringVO

class Country(StringVO):
    def __init__(self, value: str):
        self._clean(value, error_msg="O código de país deve ser uma string")
        super().__init__(value)

    def _validate(self):
        if not re.fullmatch(r"[A-Z]{2}", self.value):
            raise ValueError("Código de país deve conter exatamente 2 letras maiúsculas")