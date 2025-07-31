from apps.shared.value_objects.base import StringVO

class Description(StringVO):
    def _validate(self):
        if not isinstance(self.value, str):
            raise ValueError("Description text must be a string")
        
        if not self.value.strip():
            raise ValueError("Descritption must not be empty or just white spaces")
        
        if len(self.value) < 5:
            raise ValueError("Description must have at least five characters")