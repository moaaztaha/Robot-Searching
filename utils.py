import pygame
import time

# colors 
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165 ,0)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)
RAL = (49, 79, 111)


class Spot:
    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        self.x = row * width
        self.y = col * width
        self.color = WHITE
        self.neighbors = []
        self.width = width
        self.total_rows = total_rows
        self.free = True

    def get_pos(self):
        return self.row, self.col

    def is_closed(self):
        return self.color == RED
    
    def is_open(self):
        return self.color == GREEN
    
    def is_barrier(self):
        return self.color == BLACK
    
    def is_start(self):
        return self.color == ORANGE

    def is_end(self):
        return self.color == TURQUOISE

    def is_thebox(self):
        return self.color == BLUE

    def is_path(self):
        return self.color == PURPLE
    
    def is_free(self):
        return self.free

    def reset(self):
        self.color = WHITE

    def make_start(self):
        self.color = ORANGE

    def make_closed(self):
        self.color = RED
    
    def make_open(self):
        self.color = GREEN
    
    def make_barrier(self):
        self.color = BLACK
    
    def make_end(self):
        self.color = TURQUOISE
    
    def make_thebox(self):
        self.color = BLUE

    def make_path(self):
        self.color = PURPLE
    
    def pick_up(self):
        self.free = False
        self.color = RAL 

    def put_down(self):
        self.free = True
        self.color = ORANGE
    
    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))

    def __lt__(self, other):
        return False

    def update_neighbors(self, grid):
        self.neighbors = []
        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier(): # down
            self.neighbors.append(grid[self.row + 1][self.col])

        if self.row > 0 and not grid[self.row - 1][self.col].is_barrier(): # up
            self.neighbors.append(grid[self.row - 1][self.col])
        
        if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_barrier(): # right
            self.neighbors.append(grid[self.row][self.col + 1])

        if self.col > 0 and not grid[self.row][self.col - 1].is_barrier(): # left
            self.neighbors.append(grid[self.row][self.col - 1])








def make_grid(rows, width):
    grid = []
    gap = width // rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            spot = Spot(i, j, gap, rows)
            grid[i].append(spot)
    
    return grid

def draw_grid(win, rows, width):
    gap = width // rows
    for i in range(rows):
        pygame.draw.line(win, GREY, (0, i * gap), (width, i * gap))
        for j in range(rows):
            pygame.draw.line(win, GREY, (j * gap, 0), (j*gap, width))

def draw(win, grid, rows, width):
    win.fill(WHITE)

    # drawing/update the spots
    for row in grid:
        for spot in row:
            spot.draw(win)

    # drawing the grid
    draw_grid(win, rows, width)
    # updating the display
    pygame.display.update()


def get_clicked_pos(pos, rows, width):
    gap = width // rows
    y, x = pos

    row = y // gap
    col = x // gap

    return row, col

def clear_grid(boxes, ROWS, width, grid, all=True, path=True, paths=None):
    
    start = None
    new_boxes = []
    barriers = []

    if all:
        grid = make_grid(ROWS, width)
        boxes.clear()
        print(f'Number of Boxes: {len(boxes)}')
    
    else:
        for row in grid:
            for spot in row:
                if spot.is_start():
                    start = spot
                elif spot in boxes:
                    new_boxes.append(spot)
                
                elif spot.is_barrier():
                    barriers.append(spot)

        # new grid
        grid = make_grid(ROWS, width)
        
        # start
        if start:
            row, col = start.get_pos()
            start = grid[row][col] 
            start.make_start()

        # boxes
        boxes.clear()
        for b in new_boxes:
            row, col = b.get_pos()
            spot = grid[row][col]
            spot.make_end()
            boxes.append(spot)
        print(f'Number of new boxes {len(new_boxes)}')
        
        # barriers
        for b in barriers:
            row, col = b.get_pos()
            grid[row][col].make_barrier()

        
        # paths
        if not path:
            new_paths = []
            for b in paths:
                row, col = b.get_pos()
                spot = grid[row][col]
                spot.make_path()
                new_paths.append(spot)
            return start, grid, boxes, new_paths

    return start, grid, boxes


def walking_robot(draw, robot, path, target, boxes, task=None):
    
    for b in path:
        # reset
        robot.reset()
        b.make_start()
        robot = b
        time.sleep(0.1)
        draw()


    
    robot = b
    if task == 'pickup':
        # check if the robot is empty
        if robot.is_free():
            robot.pick_up()
            target.reset()
            boxes.remove(target)
            #boxes.remove(target)



    return robot, boxes
