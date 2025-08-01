from apps.shared.value_objects.base import StringVO
import re

class PostalCode(StringVO):
    def __init__(self, value: str):
        value = value.strip()
        super().__init__(value)

    def _validate(self):
        if not isinstance(self.value, str):
            raise ValueError("Código postal deve ser uma string")

        # Aceita letras, números, espaços e hífens (ex: K1A 0B1 ou 12345-6789)
        if not re.fullmatch(r"[A-Za-z0-9\- ]{3,10}", self.value):
            raise ValueError("Código postal inválido: deve conter de 3 a 10 caracteres alfanuméricos")