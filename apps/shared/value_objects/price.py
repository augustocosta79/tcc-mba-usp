from apps.shared.value_objects.base import NumericVO
from decimal import Decimal

class Price(NumericVO):
    def _validate(self):
        if self.value < 0:
            raise ValueError("Negative price is not allowed")
        
    def __str__(self):
        return f"R${self.value}"

    def __mul__(self, other):
        if isinstance(other, (int, float, Decimal)):
            return Price(self.value * Decimal(str(other)))
        if isinstance(other, Price):
            return Price(self.value * other.value)
        raise TypeError(f"Cannot multiply Price with {type(other)}")

    def __rmul__(self, other):
        return self.__mul__(other)

    def __radd__(self, other):
        # necessário para sum() funcionar, que começa com 0
        if other == 0:
            return self
        return self.__add__(other)