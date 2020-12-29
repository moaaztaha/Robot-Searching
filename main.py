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
    target = None
    boxes = []
    targets = []

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
                    start, grid = clear_grid(grid, all=False)
                    
                    for row in grid:
                        for spot in row:
                            spot.update_neighbors(grid)

                    path, end = algorithm(lambda: draw(win, grid, ROWS, width), grid, start, end, boxes, targets)
                    # if the algorithm found a path
                    if path:
                        print('got the path')
                        # clear the opened and colosed spots
                        start, grid = clear_grid(grid, all=False, path=False)
                        # Walking the robot
                        start, boxes = walking_robot(lambda: draw(win, grid, ROWS, width), start, path, end, boxes, task='pickup')
                        # re-coloring the targets
                        for t in targets:
                            t.make_target()
                        # switch to searching for target locations
                
                # Changing algorithm
                if event.key == pygame.K_LCTRL:
                    algorithm = next(algorithms)
                    print(f'Current Algorithm {algorithm.__name__}')
                    # clearing the grid except for start, boxes and barriers
                    time.sleep(0.4)
                    start, grid, boxes = clear_grid(boxes, targets, grid, all=False)


                # clearing the grid
                if event.key == pygame.K_c:
                    start, grid = clear_grid(grid)
                    boxes.clear()
                    targets.clear()


                # Adding A Robot
                if event.key == pygame.K_r:
                    #if pygame.mouse.get_pressed()[0]: # left mouse click
                    pos = pygame.mouse.get_pos()
                    row, col = get_clicked_pos(pos, ROWS, width)
                    spot = grid[row][col]
                
                    if not start and spot not in boxes and spot not in targets:
                        start = spot
                        start.make_start()

                # Adding boxes
                if event.key == pygame.K_b:
                    #if pygame.mouse.get_pressed()[0]: # left mouse click
                    pos = pygame.mouse.get_pos()
                    row, col = get_clicked_pos(pos, ROWS, width)
                    spot = grid[row][col]
                
                    if spot != start and spot != end and spot not in boxes and spot not in targets:
                        end = spot
                        end.make_end()
                        boxes.append(end)
                        print(f'Number of Boxes: {len(boxes)}')
                
                # Adding Targets
                if event.key == pygame.K_t:
                    pos = pygame.mouse.get_pos()
                    row, col = get_clicked_pos(pos, ROWS, width)
                    spot = grid[row][col]

                    if spot != start and spot != end and spot not in boxes and spot not in targets:
                        target = spot
                        target.make_target()
                        targets.append(target)
                        print(f'Number of Targets {len(targets)}')


                # Adding Barriers
                if event.key == pygame.K_p:
                    pos = pygame.mouse.get_pos()
                    row, col = get_clicked_pos(pos, ROWS, width)
                    spot = grid[row][col]

                    if spot != start and spot not in boxes and spot not in targets:
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
                elif spot in targets:
                    targets.remove(spot)
                    target = None


                print(f'Number of Boxes  : {len(boxes)}')
                print(f'Number of Targets: {len(targets)}')
    
    # quit the window if it exits the while loop
    pygame.quit()

main(WIN, WIDTH)