from apps.shared.value_objects.base import NumericVO

class Stock(NumericVO):
    def _validate(self):
        if not self.is_integer():
            raise ValueError("The stock value must be an integer number")
        
        if self.value < 0:
            raise ValueError("The stock value must be greater or equal zero")