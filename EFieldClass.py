'''
William Tang (wyt)
Created 7/6/2021
'''

import FieldClass
class EField(FieldClass.Field):
    def __init__(self, direction = None):
        self.direction = direction
    
    def __eq__(self, other):
        return (isinstance(other, EField) and self.direction == other.direction)