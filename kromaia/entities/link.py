class Link(object):
    def __init__(self, hullIndexFirst, hullIndexSecond):
        self.hullIndexFirst = hullIndexFirst
        self.hullIndexSecond = hullIndexSecond

    def __repr__(self):
        return f"Link(hullIndexFirst: {self.hullIndexFirst}, hullIndexSecond: {self.hullIndexSecond})"
