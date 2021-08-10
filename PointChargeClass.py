class PointCharge(object):
    def __init__(self, cx, cy, velocityDirection = None, 
            charge = '+'):
        # cx and cy stored in graphics form
        self.cx = cx
        self.cy = cy
        self.velocityDirection = velocityDirection
        self.charge = charge
    
    @staticmethod
    def getOppositeDirection(directionIn):
        if directionIn == 'R':
            return 'L'
        elif directionIn == 'L':
            return 'R'
        elif directionIn == 'U':
            return 'D'
        elif directionIn == 'D':
            return 'U'
        elif directionIn == 'I':
            return 'O'
        elif directionIn == 'O':
            return 'I'