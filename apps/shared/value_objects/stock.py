class Stock:
    def __init__(self, value: int):
        self.value = value
        self._validate()

    def _validate(self):
        if not isinstance(self.value, int):
            raise ValueError("The stock value must be an integer number")
        
        if self.value < 0:
            raise ValueError("The stock value must be greater or equal zero")
        
    def __add__(self, other_stock):
        if isinstance(other_stock, Stock):
            return self.value + other_stock.value
    
    def __sub__(self, other_stock):
        if isinstance(other_stock, Stock):
            return self.value - other_stock.value
    
    def __str__(self):
        return self.value
    
    def __eq__(self, other):
        return isinstance(other, Stock) and self.value == other.value
    
    def __hash__(self):
        return hash(self.value)