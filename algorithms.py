from queue import PriorityQueue, Queue
import pygame
import time
import math


def astar(draw, grid, start, end, boxes, targets, goal):
    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start))
    came_from = {}
    g_score = {spot: float('inf') for row in grid for spot in row}
    g_score[start] = 0
    f_score = {spot: float('inf') for row in grid for spot in row}
    print('The First end!')
    if goal == 'target':
        end = closest_box(start, targets, goal)
    # the closest box
    else:
        end = closest_box(start, boxes, goal)
    f_score[start] = h(start.get_pos(), end.get_pos())

    open_set_hash = {start}
    # the closest box
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
            path = reconstruct_path(came_from, end, draw)
            end.make_thebox()
            start.make_start()
            draw()
            return path, end

        if goal == 'target':
            end = closest_box(current, targets, goal)
        # the closest box
        else:
            end = closest_box(current, boxes, goal)

        # Going through all the neighbors of the current node, calculating the g, f scores and adding them to the PriorityQueue
        for neighbor in current.neighbors:
            temp_g_score = g_score[current] + 1  # the current g_score + 1

            # if our temp g_score for the neighbor node  < the neighbor's g_score: shortest path
            if temp_g_score < g_score[neighbor]:
                # update the came_from dictionary
                came_from[neighbor] = current
                # update the neighbor's g_score
                g_score[neighbor] = temp_g_score
                # calculates the neighbor's new f_score
                f_score[neighbor] = temp_g_score + \
                    h(neighbor.get_pos(), end.get_pos())
                if neighbor not in open_set_hash:  # if not in the PriorityQueue: Add it
                    count += 1
                    # put the node in the PriorityQueue
                    open_set.put((f_score[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)
                    # don't re-color boxes
                    if neighbor not in boxes and neighbor not in targets:
                        neighbor.make_open()

        # print(f'F_score: {current_list[0]} \t Count: {current_list[1]} \t x: {current.get_pos()[0]} \t y: {current.get_pos()[1]}')
        # print('_'*50)
        time.sleep(.1)
        draw()

        # if it's not the start node, close it
        if current != start:
            current.make_closed()

    print('No solution found')
    return False, False


def bfs(draw, grid, start, end, boxes, targets, goal=None):
    came_from = {}
    q = Queue()
    q.put(start)

    visited = [start]

    current = None

    while not q.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()


        current = q.get()

        if goal == 'target':
            end = closest_box(current, targets, goal)
        # the closest box
        else:
            end = closest_box(current, boxes, goal)

        for neighbor in current.neighbors:
            if neighbor not in visited:
                q.put(neighbor)
                visited.append(neighbor)
                came_from[neighbor] = current
                # don't re-color boxes
                if neighbor not in boxes and neighbor not in targets:
                    neighbor.make_open()
                time.sleep(.05)

        if current != start:
            current.make_closed()
        draw()

        if current == end:
            path = reconstruct_path(came_from, end, draw)
            end.make_thebox()
            start.make_start()
            draw()
            return path, end
        # time.sleep(1)
    return False, False

# heurstic function -> can be replaced with Euclidian distance or something else


def h(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)
    # return math.sqrt((y2-y1)**2 + (x2-x1)**2)


def reconstruct_path(came_from, current, draw):
    path = []
    while current in came_from:
        current = came_from[current]
        path.append(current)
        # current.make_path()
        # draw()

    path = list(reversed(path[:-1]))
    for spot in path:
        spot.make_path()
        draw()
        time.sleep(0.1)

    return path


def closest_box(current, boxes, goal):
    min_distance = float('inf')
    for box in boxes:
        current_distance = h(box.get_pos(), current.get_pos())
        if current_distance <= min_distance:
            min_distance = current_distance
            end = box
            #print('New end is assigned')
            box.make_thebox()
            for b in boxes:
                if b != box:
                    if goal == 'target':
                        b.make_target()
                    else:
                        b.make_end()
    return end
