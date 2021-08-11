import FieldClass
class BField(FieldClass.Field):
    def __init__(self, direction = None):
        self.direction = direction
    
    def __eq__(self, other):
        return (isinstance(other, BField) and self.direction == other.direction)

    def __repr__(self):
        return self.direction