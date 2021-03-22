class Link(object):
    def __init__(self, hull_index_first, hull_index_second):
        self.hull_index_first = hull_index_first
        self.hull_index_second = hull_index_second

    def __repr__(self):
        return f"Link(hull_index_first: {self.hull_index_first}, hull_index_second: {self.hull_index_second})"
