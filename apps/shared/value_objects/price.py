from typing import Union
from decimal import Decimal

class Price:
    def __init__(self, value: Union[str, int, float, Decimal]):
        self.value = Decimal(str(value))

    def validate(self):
        if self.value < 0:
            raise ValueError("Negative price is not allowed")
        
    def __str__(self):
        return f"R${self.value}"
    
    def __add__(self, other_price):
        if isinstance(other_price, Price):
            return self.value + other_price.value


    def __sub__(self, other_price):
        if isinstance(other_price, Price):
            return self.value - other_price.value
        
    def __hash__(self):
        return hash(self.value)
    
    def __eq__(self, other):
        return isinstance(other, Price) and self.value == other.value