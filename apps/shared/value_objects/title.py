from apps.shared.value_objects.base import StringVO
class Title(StringVO):
    def _validate(self):
        if not isinstance(self.value, str):
            raise ValueError("The text title must be a string")
        
        if len(self.value) < 2:
            raise ValueError("Title text must have more than two characters")