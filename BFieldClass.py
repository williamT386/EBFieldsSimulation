class BField(object):
    def __init__(self, direction = None, wireCause = None):
        self.direction = direction
        self.wireCause = wireCause
    
    def __eq__(self, other):
        return (isinstance(other, BField) and self.direction == other.direction and
                self.wireCause == other.wireCause)