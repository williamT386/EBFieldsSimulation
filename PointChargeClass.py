'''
William Tang (wyt)
Created 7/6/2021
'''

class PointCharge(object):
    def __init__(self, cx, cy, velocityDirection = None, 
            charge = '+'):
        # cx and cy stored in graphics form
        self.cx = cx
        self.cy = cy
        self.velocityDirection = velocityDirection
        self.charge = charge