'''
William Tang (wyt)
Created 7/6/2021
'''

import FieldClass
class BField(FieldClass.Field):
    # Initializes the values for this BField
    def __init__(self, direction = None):
        self.direction = direction
    
    # Compares to see if this EField is equal to another BField
    def __eq__(self, other):
        return (isinstance(other, BField) and self.direction == other.direction)