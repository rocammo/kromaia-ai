class Hull(object):
    def __init__(self, scale, position, orientation):
        self.scale = scale
        self.position = position
        self.orientation = orientation

    def __repr__(self):
        return f"Hull(scale: <{self.scale}>, position: <{self.position}>, orientation: <{self.orientation}>)"
