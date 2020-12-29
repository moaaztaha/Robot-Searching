# modules
import pygame
from algorithms import astar, bfs
from utils import Spot, make_grid, draw, get_clicked_pos, clear_grid, walking_robot
import itertools
import time


WIDTH = 800
WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("Robot!!")



def main(win, width):
    ROWS = 10
    grid = make_grid(ROWS, width)

    start = None
    end = None
    boxes = []

    # default algorithm
    algorithms = itertools.cycle([astar, bfs])
    algorithm = next(algorithms)
    print(f'Current Algorithm {algorithm.__name__}')

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
                if event.key == pygame.K_SPACE and start and len(boxes):
                    # clearing the grid except for start, boxes and barriers
                    start, grid, boxes = clear_grid(boxes, ROWS, width, grid, all=False)
                    
                    for row in grid:
                        for spot in row:
                            spot.update_neighbors(grid)

                    path, end = algorithm(lambda: draw(win, grid, ROWS, width), grid, start, end, boxes)
                    # if the algorithm found a path
                    if path:
                        print('got the path')
                        # clear the opened and colosed spots
                        start, grid, boxes, paths = clear_grid(boxes, ROWS, width, grid, all=False, path=False, paths=path)
                        # Walking the robot
                        # the new end in the new grid
                        row, col = end.get_pos()
                        end = grid[row][col]
                        start, boxes = walking_robot(lambda: draw(win, grid, ROWS, width), start, paths, end, boxes, task='pickup')
                        end.reset()
                        # switch to searching for target locations
                
                # Changing algorithm
                if event.key == pygame.K_LCTRL:
                    algorithm = next(algorithms)
                    print(f'Current Algorithm {algorithm.__name__}')
                    # clearing the grid except for start, boxes and barriers
                    time.sleep(0.4)
                    start, grid, boxes = clear_grid(boxes, ROWS, width, grid, all=False)


                # clearing the grid
                if event.key == pygame.K_c:
                    start, grid, boxes = clear_grid(boxes, ROWS, width, grid)


                # Adding A Robot
                if event.key == pygame.K_r:
                    #if pygame.mouse.get_pressed()[0]: # left mouse click
                    pos = pygame.mouse.get_pos()
                    row, col = get_clicked_pos(pos, ROWS, width)
                    spot = grid[row][col]
                
                    if not start and spot not in boxes and not spot.is_barrier():
                        start = spot
                        start.make_start()

                # Adding boxes
                if event.key == pygame.K_b:
                    #if pygame.mouse.get_pressed()[0]: # left mouse click
                    pos = pygame.mouse.get_pos()
                    row, col = get_clicked_pos(pos, ROWS, width)
                    spot = grid[row][col]
                
                    if spot != start and spot != end and spot not in boxes:
                        end = spot
                        end.make_end()
                        boxes.append(end)
                        print(f'Number of Boxes: {len(boxes)}')


                # Adding Barriers
                if event.key == pygame.K_p:
                    pos = pygame.mouse.get_pos()
                    row, col = get_clicked_pos(pos, ROWS, width)
                    spot = grid[row][col]

                    if spot != start and spot not in boxes:
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
                    end = None

                print(f'Number of Boxes: {len(boxes)}')
    
    # quit the window if it exits the while loop
    pygame.quit()

main(WIN, WIDTH)