from apps.shared.value_objects.base import StringVO
class Complement(StringVO):
    def _validate(self):
        if not len(self.value.strip()) > 0:
            raise ValueError("Complement can not be empty.")
