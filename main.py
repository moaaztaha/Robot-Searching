# modules
import pygame
from queue import PriorityQueue, Queue
import time
import math


WIDTH = 800
WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("Robot!!")

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


# heurstic function -> can be replaced with Euclidian distance or something else        
def h(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    #return abs(x1 - x2) + abs(y1 - y2)
    return math.sqrt((y2-y1)**2 + (x2-x1)**2)

def reconstruct_path(came_from, current, draw):
    while current in came_from:
        current = came_from[current]
        current.make_path()
        draw()

def algorithm(draw, grid, start , end):
    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start))
    came_from = {}
    g_score = {spot: float('inf') for row in grid for spot in row}
    g_score[start] = 0
    f_score = {spot: float('inf') for row in grid for spot in row}
    f_score[start] = h(start.get_pos(), end.get_pos())

    open_set_hash = {start}
    # the closest box
    min_distance = float('inf')
    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()


        # get the node on the top (the one with the shortest F score)
        current_list = open_set.get()
        current = current_list[2]

        open_set_hash.remove(current) 

        # if we found the target
        if current == end:
            reconstruct_path(came_from, end, draw)
            end.make_thebox()
            start.make_start()
            return True



        for box in boxes:
            current_distance = h(box.get_pos(), current.get_pos())
            if current_distance <= min_distance:
                min_distance = current_distance
                end = box
                box.make_thebox()
                for b in boxes: 
                    if b != box: b.make_end()

        # Going through all the neighbors of the current node, calculating the g, f scores and adding them to the PriorityQueue
        for neighbor in current.neighbors:
            temp_g_score = g_score[current] + 1 # the current g_score + 1
            
            # if our temp g_score for the neighbor node  < the neighbor's g_score: shortest path
            if temp_g_score < g_score[neighbor]:
                came_from[neighbor] = current # update the came_from dictionary
                g_score[neighbor] = temp_g_score # update the neighbor's g_score 
                f_score[neighbor] = temp_g_score + h(neighbor.get_pos(), end.get_pos()) # calculates the neighbor's new f_score
                if neighbor not in open_set_hash: # if not in the PriorityQueue: Add it
                    count += 1
                    open_set.put((f_score[neighbor], count, neighbor)) # put the node in the PriorityQueue
                    open_set_hash.add(neighbor)
                    neighbor.make_open()
        
        print(f'F_score: {current_list[0]} \t Count: {current_list[1]} \t x: {current.get_pos()[0]} \t y: {current.get_pos()[1]}')
        print('_'*50)
        time.sleep(.1)
        draw()

        # if it's not the start node, close it
        if current != start:
            current.make_closed()
    
    return False

boxes = []
def bfs(draw, grid, start, end):
    came_from = {}
    q = Queue()
    q.put(start)

    visited = [start]

    current = None

    while not q.empty(): 
        current = q.get()
        
        # the closest box
        min_distance = float('inf')
        for box in boxes:
            current_distance = h(box.get_pos(), current.get_pos())
            if current_distance < min_distance:
                min_distance = current_distance
                end = box
                box.make_thebox()
                for b in boxes: 
                    if b != box: b.make_end()


        for neighbor in current.neighbors:
            if neighbor not in visited:
                q.put(neighbor)
                visited.append(neighbor)
                came_from[neighbor] = current
                # don't re-color boxes
                if neighbor not in boxes:
                    neighbor.make_open()
                time.sleep(.2)

        if current != start:
            current.make_closed()
        draw()

        if current == end:
            reconstruct_path(came_from, end, draw)
            end.make_thebox()
            start.make_start()
            return True   
        #time.sleep(1)
    return False


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

def main(win, width):
    ROWS = 10
    grid = make_grid(ROWS, width)

    start = None
    end = None

    run = True
    while run:
        draw(win, grid, ROWS, width)
        for event in pygame.event.get():
            # quitting the window
            if event.type == pygame.QUIT:
                run = False

            # keyboard events
            if event.type == pygame.KEYDOWN:
                # the algorithm
                if event.key == pygame.K_SPACE and start and end:
                    for row in grid:
                        for spot in row:
                            spot.update_neighbors(grid)

                    bfs(lambda: draw(win, grid, ROWS, width), grid, start, end)
                
                # clearing the grid
                if event.key == pygame.K_c:
                    start = None
                    end = None
                    grid = make_grid(ROWS, width)


                # Adding A Robot
                if event.key == pygame.K_r:
                    #if pygame.mouse.get_pressed()[0]: # left mouse click
                    pos = pygame.mouse.get_pos()
                    row, col = get_clicked_pos(pos, ROWS, width)
                    spot = grid[row][col]
                
                    if not start:
                        start = spot
                        start.make_start()

                # Adding boxes
                if event.key == pygame.K_b:
                    #if pygame.mouse.get_pressed()[0]: # left mouse click
                    pos = pygame.mouse.get_pos()
                    row, col = get_clicked_pos(pos, ROWS, width)
                    spot = grid[row][col]
                
                    end = spot
                    end.make_end()
                    boxes.append(end)

                # Adding Barriers
                if event.key == pygame.K_p:
                    pos = pygame.mouse.get_pos()
                    row, col = get_clicked_pos(pos, ROWS, width)
                    spot = grid[row][col]

                    if spot != start and spot != end:
                        spot.make_barrier()

            # clearning spots
            if pygame.mouse.get_pressed()[2]: # right mouse click
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, width)
                spot = grid[row][col]
                spot.reset()
                if spot == start:
                    start = None
                elif spot in boxes:
                    boxes.remove(spot)
                    if end == spot:
                        end = boxes[0]
    
    # quit the window if it exits the while loop
    pygame.quit()



main(WIN, WIDTH)