import random

class Room(object):

    def __init__(self, size_bounds, pos_bounds):
        w = random.randint(size_bounds[0], size_bounds[1])
        h = random.randint(size_bounds[0], size_bounds[1])
        x = random.randint(1, (pos_bounds[0] - w - 1))
        y = random.randint(1, (pos_bounds[1] - h - 1))
        self.x = x
        self.y = y
        self.width = w
        self.height = h
    
    def overlaps(self, other_rooms):
        for other_room in other_rooms:
            if (
                self.x < (other_room.x + other_room.width) and 
                other_room.x < (self.x + self.width) and
                self.y < (other_room.y + other_room.height) and
                other_room.y < (self.y + self.height)
            ):
                return True
        return False

class Spur(object):

    def __init__(self, pos_bounds):
        x = random.randint(2, (pos_bounds[0] - 2))
        y = random.randint(2, (pos_bounds[1] - 2))
        self.x = x
        self.y = y
        self.width = 1
        self.height = 1 