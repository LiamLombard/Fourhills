from __future__ import print_function
from room import Room, Spur
from corridor import Corridor
import random
import png
 
CHARACTER_TILES = {'stone': ' ',
                   'floor': '.',
                   'wall': '#'}

PNG_TILES = {'stone': [0,0,0],
            'floor': [255,255,255],
            'wall': [100, 100, 100],
            'door': [100, 0, 0]
            }

 
class Generator():
    def __init__(self, width=64, height=64, max_rooms=15, min_room_xy=5,
                 max_room_xy=10, rooms_overlap=False, random_connections=1,
                 random_spurs=3, tiles=CHARACTER_TILES):
        self.width = width
        self.height = height
        self.max_rooms = max_rooms
        self.min_room_xy = min_room_xy
        self.max_room_xy = max_room_xy
        self.rooms_overlap = rooms_overlap
        self.random_connections = random_connections
        self.random_spurs = random_spurs
        self.tiles = tiles
        self.level = []
        self.room_list = []
        self.corridor_list = []
        self.tiles_level = []
 
    def join_rooms(self, room_1, room_2, join_type='either'):
        # sort by the value of x
        if room_1.x > room_2.x:
            tmp_room = room_1
            room_1 = room_2
            room_2 = tmp_room

        x1 = room_1.x
        y1 = room_1.y
        w1 = room_1.width
        h1 = room_1.height
        x1_2 = room_1.x2
        y1_2 = room_1.y2

        x2 = room_2.x
        y2 = room_2.y
        w2 = room_2.width
        h2 = room_2.height
        x2_2 = room_2.x2
        y2_2 = room_2.y2

        # overlapping on x
        if x1 < (x2 + w2) and x2 < (x1 + w1):
            jx1 = random.randint(x2, x1_2)
            jx2 = jx1
            tmp_y = [y1, y2, y1_2, y2_2]
            tmp_y.sort()
            jy1 = tmp_y[1] + 1
            jy2 = tmp_y[2] - 1
 
            corridors = Corridor(jx1, jy1, jx2, jy2, self.width, self.height)
            self.corridor_list.append(corridors)
 
        # overlapping on y
        elif y1 < (y2 + h2) and y2 < (y1 + h1):
            if y2 > y1:
                jy1 = random.randint(y2, y1_2)
                jy2 = jy1
            else:
                jy1 = random.randint(y1, y2_2)
                jy2 = jy1
            tmp_x = [x1, x2, x1_2, x2_2]
            tmp_x.sort()
            jx1 = tmp_x[1] + 1
            jx2 = tmp_x[2] - 1
 
            corridors = Corridor(jx1, jy1, jx2, jy2, self.width, self.height)
            self.corridor_list.append(corridors)
 
        # no overlap
        else:
            join = None
            if join_type is 'either':
                join = random.choice(['top', 'bottom'])
            else:
                join = join_type
 
            if join is 'top':
                if y2 > y1:
                    jx1 = x1_2 + 1
                    jy1 = random.randint(y1, y1_2)
                    jx2 = random.randint(x2, x2_2)
                    jy2 = y2 - 1
                    corridors = Corridor(jx1, jy1, jx2, jy2, self.width, self.height, 'bottom')
                    self.corridor_list.append(corridors)
                else:
                    jx1 = random.randint(x1, x1_2)
                    jy1 = y1 - 1
                    jx2 = x2 - 1
                    jy2 = random.randint(y2, y2_2)
                    corridors = Corridor(jx1, jy1, jx2, jy2, self.width, self.height, 'top')
                    self.corridor_list.append(corridors)
 
            elif join is 'bottom':
                if y2 > y1:
                    jx1 = random.randint(x1, x1_2)
                    jy1 = y1_2 + 1
                    jx2 = x2 - 1
                    jy2 = random.randint(y2, y2_2)
                    corridors = Corridor(jx1, jy1, jx2, jy2, self.width, self.height, 'top')
                    self.corridor_list.append(corridors)
                else:
                    jx1 = x1_2 + 1
                    jy1 = random.randint(y1, y1_2)
                    jx2 = random.randint(x2, x2_2)
                    jy2 = y2_2 + 1
                    corridors = Corridor(jx1, jy1, jx2, jy2, self.width, self.height, 'bottom')
                    self.corridor_list.append(corridors)
 
 
    def gen_level(self):
 
        # build an empty dungeon, blank the room and corridor lists
        for i in range(self.height):
            self.level.append(['stone'] * self.width)
        self.room_list = []
        self.corridor_list = []
 
        max_iters = self.max_rooms * 5
 
        for a in range(max_iters):
            tmp_room = Room(
                [self.min_room_xy, self.max_room_xy], 
                [self.width, self.height]
              )
 
            if self.rooms_overlap or not self.room_list:
                self.room_list.append(tmp_room)
            else:
                tmp_room = Room(
                    [self.min_room_xy, self.max_room_xy], 
                    [self.height, self.width]
                  )
 
                if not tmp_room.overlaps(self.room_list):
                    self.room_list.append(tmp_room)
 
            if len(self.room_list) >= self.max_rooms:
                break
 
        # connect the rooms
        for a in range(len(self.room_list) - 1):
            self.join_rooms(self.room_list[a], self.room_list[a + 1])
 
        # do the random joins
        for a in range(self.random_connections):
            room_1 = self.room_list[random.randint(0, len(self.room_list) - 1)]
            room_2 = self.room_list[random.randint(0, len(self.room_list) - 1)]
            self.join_rooms(room_1, room_2)
 
        # do the spurs
        for a in range(self.random_spurs):
            room_1 = Spur([self.width, self.height])
            room_2 = self.room_list[random.randint(0, len(self.room_list) - 1)]
            self.join_rooms(room_1, room_2)
 
        # fill the map
        # paint rooms
        for room_num, room in enumerate(self.room_list):
            for b in range(room.width):
                for c in range(room.height):
                    self.level[room.y + c][room.x+ b] = 'floor'
 
        # paint corridors
        # TODO add doors
        for corridor in self.corridor_list:
            x1, y1 = corridor.points[0]
            x2, y2 = corridor.points[1]
            for width in range(abs(x1 - x2) + 1):
                for height in range(abs(y1 - y2) + 1):
                    self.level[min(y1, y2) + height][
                        min(x1, x2) + width] = 'floor'
 
            if len(corridor.points) == 3:
                x3, y3 = corridor.points[2]
 
                for width in range(abs(x2 - x3) + 1):
                    for height in range(abs(y2 - y3) + 1):
                        self.level[min(y2, y3) + height][
                            min(x2, x3) + width] = 'floor'
 
        # paint the walls
        for row in range(1, self.height - 1):
            for col in range(1, self.width - 1):
                if self.level[row][col] == 'floor':
                    if self.level[row - 1][col - 1] == 'stone':
                        self.level[row - 1][col - 1] = 'wall'
 
                    if self.level[row - 1][col] == 'stone':
                        self.level[row - 1][col] = 'wall'
 
                    if self.level[row - 1][col + 1] == 'stone':
                        self.level[row - 1][col + 1] = 'wall'
 
                    if self.level[row][col - 1] == 'stone':
                        self.level[row][col - 1] = 'wall'
 
                    if self.level[row][col + 1] == 'stone':
                        self.level[row][col + 1] = 'wall'
 
                    if self.level[row + 1][col - 1] == 'stone':
                        self.level[row + 1][col - 1] = 'wall'
 
                    if self.level[row + 1][col] == 'stone':
                        self.level[row + 1][col] = 'wall'
 
                    if self.level[row + 1][col + 1] == 'stone':
                        self.level[row + 1][col + 1] = 'wall'
 
    def gen_tiles_level(self):
        for row_num, row in enumerate(self.level):
            temp_row = []
            for col_num, col in enumerate(row):
                temp_row.extend(self.tiles[col])
            self.tiles_level.append(tuple(temp_row))
 
        self.print_map()
    
    def print_map(self): 
        with open('map.png', 'wb') as f:
            w = png.Writer(self.width, self.height, greyscale=False)
            w.write(f, self.tiles_level)
 
 
if __name__ == '__main__':
    gen = Generator(tiles=PNG_TILES)
    gen.gen_level()
    gen.gen_tiles_level()