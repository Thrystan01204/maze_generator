def get_neighbors(
    cell_idx: int, c_walls: list[int], r_walls: list[int], width: int, height: int
) -> list[int]:
    neighbors = []
    cell_row, cell_col = divmod(cell_idx, width)

    if 0 <= cell_col < width - 1 and not c_walls[cell_row * (width - 1) + cell_col]:
        neighbors.append(cell_idx + 1)

    if 0 < cell_col <= width - 1 and not c_walls[cell_row * (width - 1) + cell_col - 1]:
        neighbors.append(cell_idx - 1)

    if 0 < cell_row <= height - 1 and not r_walls[cell_idx - width]:
        neighbors.append(cell_idx - width)

    if 0 <= cell_row < height - 1 and not r_walls[cell_idx]:
        neighbors.append(cell_idx + width)

    return neighbors


def dijkstra(
    start_cell_index: int,
    r_walls: list[int],
    c_walls: list[int],
    width: int,
    height: int,
) -> list[float]:
    weights = [float("inf") for _ in range(width * height)]
    weights[start_cell_index] = 0

    visited = [False for _ in range(width * height)]
    visited[start_cell_index] = True

    queue = [start_cell_index]

    while queue:
        current_cell_idx = min(queue, key=lambda weight: weights[weight])
        current_cell_weight = weights[current_cell_idx]
        neighbors = get_neighbors(current_cell_idx, c_walls, r_walls, width, height)

        for neighbor in neighbors:
            weights[neighbor] = min(current_cell_weight + 1, weights[neighbor])
            if neighbor not in queue and not visited[neighbor]:
                queue.append(neighbor)
                visited[neighbor] = True

        queue.remove(current_cell_idx)

    return weights
