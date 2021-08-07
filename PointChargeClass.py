class PointCharge(object):
    def __init__(self, cx, cy, velocity = 0, velocityDirection = None, 
            charge = '+'):
        self.cx = cx
        self.cy = cy
        self.velocity = velocity
        self.velocityDirection = velocityDirection
        self.charge = charge
    