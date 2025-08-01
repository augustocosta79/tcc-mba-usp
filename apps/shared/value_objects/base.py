    #### Em DDD Value Objects:
    #          1) não tem identidade;
    #          2) São definidos apenas por seu valor;
    #          3) devem ser comparaveis por valor, não por instância  

from abc import ABC, abstractmethod
from decimal import Decimal
from typing import Any, Union


class StringVO(ABC):
    def __init__(self, value: str):
        self.value = value
        self._validate()

    @abstractmethod
    def _validate(self):
        pass

    
    def _clean(self, raw_value: Any, *, error_msg: str) -> str:
        if not isinstance(raw_value, str):
            raise ValueError(error_msg)
        return raw_value

    def __str__(self): # para poder imprimir o valor
        return self.value

    def __eq__(self, other): # para poder fazer compração de objetos por valores em vez de ref na memoria
        return isinstance(other, self.__class__) and self.value == other.value

    def __hash__(self): # para poder ser usado como chave de dict e sem set() para remover duplicatas
        return hash(self.value)


class NumericVO(ABC):
    def __init__(self, value: Union[str, int, float, Decimal]):
        self.value = Decimal(str(value))
        self._validate()

    @abstractmethod
    def _validate(self):
        pass

    def is_integer(self) -> bool:
        return self.value == self.value.to_integral_value()

    def __add__(self, other):
        if isinstance(other, self.__class__):
            return self.value + other.value

    def __sub__(self, other):
        if isinstance(other, self.__class__):
            return self.value - other.value

    def __str__(self):
        return str(self.value)

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.value == other.value

    def __hash__(self):
        return hash(self.value)
