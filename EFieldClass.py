import PointChargeClass
class EField(object):
    def __init__(self, direction = None, pointChargeCause = None):
        self.direction = direction
        self.pointChargeCause = pointChargeCause
    def __eq__(self, other):
        return (isinstance(other, EField) and self.direction == other.direction and
                self.pointChargeCause == other.pointChargeCause)