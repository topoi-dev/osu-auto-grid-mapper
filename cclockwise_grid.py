# osu Grid size = 384x512
# using multiples of 16 for snapping
# center is 192x256

# want to use 32 pixels off the edges of the grid
# so grid size will start at 32,32 and end 352,480

grid_start_x = 32
grid_start_y = 32
grid_end_x = 352
grid_end_y = 480

from enum import Enum
import random

class Direction(Enum):
    NORTH = 0
    EAST = 1
    SOUTH = 2
    WEST = 3

def check_overflow(a, b): 
    return True if (a > b) else False 

def try_direction(dir, x, y, d):
    # check if x and y are in bounds
    if (dir == 0):
        if (y - d >= grid_start_y):
            return True
    elif (dir == 1):
        if (x + d <= grid_end_x):
            return True
    elif (dir == 2):
        if (y + d <= grid_end_y):
            return True
    elif (dir == 3):
        if (x - d >= grid_start_x):
            return True
    
    return False

def go_direction(dir,x,y,d):
    if (dir == 0):
        y -= d
    elif (dir == 1):
        x += d
    elif (dir == 2):
        y += d
    elif (dir == 3):
        x -= d

    return x,y

def map_cclockwise_grid(snapped_timings, bpm_interval, g_size=32):
    print('Mapping notes to grid...')
    # counter clockwise = 3, clockwise = 1
    clockwise = True
    cwise_counter = 0
    cwise_interval = 3

    dir_value = 1
    cur_direction = Direction(dir_value)
    cur_x = 192
    cur_y = 256

    note_locations = [[cur_x,cur_y]]

    previous_note = 0
    for note in snapped_timings[1:]:

        distance = (note - snapped_timings[previous_note]) / bpm_interval
        distance = round(distance) * g_size
        previous_note+=1

        # attempt all 4 directions
        counter = 0
        attempt_dir_val = cur_direction.value
        while(counter < 4):
            valid = try_direction(attempt_dir_val,cur_x,cur_y, distance)
            if valid:
                cur_x, cur_y = go_direction(attempt_dir_val, cur_x, cur_y, distance)
                if (clockwise): dir_value = (attempt_dir_val + 1) % 4
                else: dir_value = (attempt_dir_val - 1) % 4
                cur_direction = Direction(attempt_dir_val)
                break
            else:
                if (clockwise): attempt_dir_val = (attempt_dir_val + 1) % 4
                else: attempt_dir_val = (attempt_dir_val - 1) % 4
            counter+=1
        
        if (counter == 4):
            # in the case you cannot distance snap in any direction, flip x and y
            # dir will not change
            cur_x = grid_end_x - cur_x
            cur_y = grid_end_y - cur_y
            clockwise = not clockwise
            
  
        cwise_counter+=1
        if (cwise_counter >= cwise_interval):
            if (clockwise): rand_inc = (cur_direction.value + 1) % 4
            else: rand_inc = (cur_direction.value -1) % 4
            
            cur_direction = Direction(rand_inc)
            clockwise = not clockwise
            cwise_counter = 0

        note_locations.append([cur_x,cur_y])
        
    return note_locations