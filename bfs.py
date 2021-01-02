from queue import Queue


def bfs(draw, grid, start, end):
    came_from = {}
    q = Queue()
    q.put(start)

    visited = [start]

    current = None

    while not q.empty():

        if current == end:
            reconstruct_path(came_from, end, draw)
            end.make_end()
            start.make_start()
            return True    

        current = q.get()
        for neighbor in current.neighbors:
            if neighbor not in visited:
                q.put(neighbor)
                visited.append(neighbor)
                came_from[neighbor] = current
                neighbor.make_open()

    if current != start:
        current.make_closed()
    return False