class Name:
    def __init__(self, value: str):
        self.value = value.strip()
        self.validate()

    def validate(self):
        if not self.value:
            raise ValueError("O nome é obrigatório.")
        
        if any(char.isdigit() for char in self.value):
            raise ValueError("O nome não pode conter números")
    
    #### Em DDD Value Objects:
    #          1) não tem identidade;
    #          2) São definidos apenas por seu valor;
    #          3) devem ser comparaveis por valor, não por instância    

    def __str__(self): # para poder imprimir o valor
        return self.value
    
    def __eq__(self, other): # para poder fazer compração de objetos por valores em vez de ref na memoria
        return isinstance(other, Name) and self.value == other.value
    
    def __hash__(self): # para poder ser usado como chave de dict e sem set() para remover duplicatas
        return hash(self.value)
