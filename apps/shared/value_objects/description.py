class Description:
    def __init__(self, text: str):
        self.text = text
        self.validate()

    def validate(self):
        if not isinstance(self.text, str):
            raise ValueError("Description text must be a string")
        
        if not self.text.strip():
            raise ValueError("Descritption must not be empty or just white spaces")
        
        if len(self.text) < 5:
            raise ValueError("Description must have at least five characters")
        
    def __str__(self):
        return self.text
    
    def __eq__(self, other_description):
        return isinstance(other_description, Description) and self.text == other_description.text
    
    def __hash__(self):
        return hash(self.text)