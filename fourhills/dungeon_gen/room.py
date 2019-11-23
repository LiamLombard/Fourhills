import random

class Room(object):

    def __init__(self, size_bounds, pos_bounds):
        self.width = random.randint(size_bounds[0], size_bounds[1])
        self.height = random.randint(size_bounds[0], size_bounds[1])
        self.x = random.randint(1, (pos_bounds[0] - self.width - 1))
        self.y = random.randint(1, (pos_bounds[1] - self.height - 1))
        self.x2 = self.x + self.width - 1
        self.y2 = self.y + self.height - 1
    
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
        self.x = random.randint(2, (pos_bounds[0] - 2))
        self.y = random.randint(2, (pos_bounds[1] - 2))
        self.width = 1
        self.height = 1
        self.x2 = self.x + self.width - 1
        self.y2 = self.y + self.height - 1