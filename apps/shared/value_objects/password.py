from django.contrib.auth.hashers import make_password, check_password
import re

class Password:
    def __init__(self, raw_password: str):
        self._validate(raw_password)
        self._hashed_password = make_password(raw_password)

    def _validate(self, raw_password: str) -> None:
        validators = [
            (lambda pwd: len(pwd) >= 8, "A senha deve ter pelo menos 8 caracteres."),
            (lambda pwd: re.search(r"[A-Z]", pwd), "A senha deve conter ao menos uma letra maiúscula."),
            (lambda pwd: re.search(r"[a-z]", pwd), "A senha deve conter ao menos uma letra minúscula."),
            (lambda pwd: re.search(r"\d", pwd), "A senha deve conter ao menos um número."),
            (lambda pwd: re.search(r"[!@#$%^&*(),.?\":{}|<>]", pwd), "A senha deve conter ao menos um símbolo especial."),
        ]

        for validate, error_message in validators:
            if not validate(raw_password):
                raise ValueError(error_message)

    def verify(self, raw_password):
        return check_password(raw_password, self._hashed_password)
    
    @classmethod
    def from_hash(cls, hashed_password: str):
        obj = cls.__new__(cls)         # cria instância sem chamar __init__
        obj._hashed_password = hashed_password
        return obj

    
    @property
    def hash(self):
        return self._hashed_password
    
    def __eq__(self, other):
        return isinstance(other, Password) and other.hash == self._hashed_password
    
    def __hash__(self):
        return hash(self._hashed_password)