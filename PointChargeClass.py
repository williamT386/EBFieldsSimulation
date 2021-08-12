'''
William Tang (wyt)
Created 7/6/2021
'''

class PointCharge(object):
    # Initializes the values for this PointCharge
    def __init__(self, cx, cy, charge = '+', velocityDirection = None):
        # cx and cy stored in graphics form
        self.cx = cx
        self.cy = cy
        self.charge = charge
        self.velocityDirection = velocityDirection