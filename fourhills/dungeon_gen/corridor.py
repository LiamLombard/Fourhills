import random

class Corridor(object):

    def __init__(self, x1, y1, x2, y2, map_width, map_height, join_type='either'):
        if x1 == x2 and y1 == y2 or x1 == x2 or y1 == y2:
            self.points = [(x1, y1), (x2, y2)]
        else:
            # 2 Corridors
            # NOTE: Never randomly choose a join that will go out of bounds
            # when the walls are added.
            join = None
            if join_type is 'either' and set([0, 1]).intersection(
                 set([x1, x2, y1, y2])):
 
                join = 'bottom'
            elif join_type is 'either' and set([map_width - 1,
                 map_width - 2]).intersection(set([x1, x2])) or set(
                 [map_height - 1, map_height - 2]).intersection(
                 set([y1, y2])):
 
                join = 'top'
            elif join_type is 'either':
                join = random.choice(['top', 'bottom'])
            else:
                join = join_type
 
            if join is 'top':
                self.points = [(x1, y1), (x1, y2), (x2, y2)]
            elif join is 'bottom':
                self.points = [(x1, y1), (x2, y1), (x2, y2)]
        
        self.has_door = random.choice([True, False, False, False])
    