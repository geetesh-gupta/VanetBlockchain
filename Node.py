class Node:

    def __init__(self, x, y, dx, dy):
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy

    def get_pos(self):
        return {'x': self.x, 'y': self.y}

    def get_velocity(self):
        return {'dx': self.dx, 'dy': self.dy}

    def set_velocity(self, dx, dy):
        self.dx = dx
        self.dy = dy
