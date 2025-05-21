from django.core.validators import validate_email
from django.core.exceptions import ValidationError
import re

EMAIL_REGEX = r"^[\w\.-]+@[\w\.-]+\.\w+$"

class Email:
    def __init__(self, value: str):
        self.value = value.strip().lower()
        self._validate()

    def _validate(self):
        
        if not re.match(EMAIL_REGEX, self.value):
            raise ValueError("Insira um email válido")
        
    def __str__(self):
        return self.value
    
    def __eq__(self, other):
        return other.value == self.value and isinstance(other, Email)
    
    def __hash__(self):
        return hash(self.value)