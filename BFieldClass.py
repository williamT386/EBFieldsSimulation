class BField(object):
    def __init__(self, direction = None):
        self.direction = direction
    
    def __eq__(self, other):
        return (isinstance(other, BField) and self.direction == other.direction)