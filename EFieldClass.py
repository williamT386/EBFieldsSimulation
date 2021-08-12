'''
William Tang (wyt)
Created 7/6/2021
'''

import FieldClass
class EField(FieldClass.Field):
    # Initializes the values for this EField
    def __init__(self, direction = None):
        self.direction = direction
    
    # Compares to see if this EField is equal to another EField
    def __eq__(self, other):
        return (isinstance(other, EField) and self.direction == other.direction)