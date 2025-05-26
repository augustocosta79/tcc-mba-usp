class Title:
    def __init__(self, text: str):
        self.text = text
        self._validate()


    def _validate(self):
        if not isinstance(self.text, str):
            raise ValueError("The text title must be a string")
        
        if len(self.text) < 2:
            raise ValueError("Title text must have more than two characters")
    
    def __str__(self):
        return self.text
    
    def __eq__(self, other_title):
        return isinstance(other_title, Title) and self.text == other_title.text
    
    def __hash__(self):
        return hash(self.text)