from apps.shared.value_objects.base import StringVO
import re

EMAIL_REGEX = r"^[\w\.-]+@[\w\.-]+\.\w+$"

class Email(StringVO):
    def __init__(self, value: str):
        value = value.strip().lower()
        super().__init__(value)

    def _validate(self):
        
        if not re.match(EMAIL_REGEX, self.value):
            raise ValueError("Insira um email válido")