from apps.shared.value_objects.base import StringVO
import re

class StateCode(StringVO):
    def _validate(self):
        if not isinstance(self.value, str):
            raise ValueError("Estado deve ser uma string")

        if not (2 <= len(self.value) <= 3):
            raise ValueError("Estado deve ter entre 2 e 3 letras")

        if not re.fullmatch(r"[A-Z]{2,3}", self.value):
            raise ValueError("Estado deve conter apenas letras maiúsculas (sem espaços ou números)")