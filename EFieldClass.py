import FieldClass
class EField(FieldClass.Field):
    def __init__(self, direction = None):
        self.direction = direction
    
    def __eq__(self, other):
        return (isinstance(other, EField) and self.direction == other.direction)