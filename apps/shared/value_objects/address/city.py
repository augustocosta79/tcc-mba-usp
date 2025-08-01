from apps.shared.value_objects.base import StringVO
import re

class City(StringVO):
    def _validate(self):
        if not isinstance(self.value, str):
            raise ValueError("Nome da cidade deve ser uma string")

        if len(self.value) < 2:
            raise ValueError("Nome da cidade deve ter pelo menos 2 caracteres")

        if len(self.value) > 100:
            raise ValueError("Nome da cidade deve ter no máximo 100 caracteres")

        if not re.fullmatch(r"[A-Za-zÀ-ÿ' -]+", self.value):
            raise ValueError("Nome da cidade contém caracteres inválidos")