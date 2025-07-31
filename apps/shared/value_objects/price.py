from apps.shared.value_objects.base import NumericVO

class Price(NumericVO):
    def _validate(self):
        if self.value < 0:
            raise ValueError("Negative price is not allowed")
        
    def __str__(self):
        return f"R${self.value}"