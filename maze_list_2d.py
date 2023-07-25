from random import shuffle
from time import process_time

from print_maze import print_grid_2d


def gen_grid(width, height):
    ids = []
    current_id = 0
    for _ in range(height):
        ids.append(list(range(current_id, current_id + width)))
        current_id += width
    return {
        "ids": ids,
        "r_walls": [[True for _ in range(width)] for _ in range(height - 1)],
        "c_walls": [[True for _ in range(width - 1)] for _ in range(height)],
        "width": width,
        "height": height,
    }


def get_id(grid, row, col):
    return grid["ids"][row][col]


def is_breakable(ids, row, col, wall_type):
    if wall_type == "r":
        if ids[row][col] == ids[row + 1][col]:
            return False
    if wall_type == "c":
        if ids[row][col] == ids[row][col + 1]:
            return False
    return True


def rewrite_ids(grid, source_id, target_id):
    ids = grid["ids"]
    for row_idx, row in enumerate(ids):
        ids[row_idx] = [
            source_id if cell_id == target_id else cell_id for cell_id in row
        ]
    return grid


def all_walls(r_walls, c_walls):
    walls = []
    idx = 0
    for row in r_walls:
        for current_idx in range(len(row)):
            walls.append(f"r{current_idx + idx}")
        idx += len(row)
    idx = 0
    for row in c_walls:
        for current_idx in range(len(row)):
            walls.append(f"c{current_idx + idx}")
        idx += len(row)
    return walls


def maze(maze_width, maze_height):
    a_grid = gen_grid(maze_width, maze_height)
    shuffle(a_grid["c_walls"])
    shuffle(a_grid["r_walls"])
    the_walls = all_walls(a_grid["r_walls"], a_grid["c_walls"])
    shuffle(the_walls)

    for wall in the_walls:
        wall_type = wall[0]
        wall_idx = int(wall[1:])
        ids = a_grid["ids"]
        if wall_type == "r":
            wall_row, wall_col = divmod(wall_idx, maze_width)
            if is_breakable(ids, wall_row, wall_col, wall_type):
                source_id = get_id(a_grid, wall_row, wall_col)
                target_id = get_id(a_grid, wall_row + 1, wall_col)
                a_grid["r_walls"][wall_row][wall_col] = False
                a_grid = rewrite_ids(a_grid, source_id, target_id)
        else:
            wall_row, wall_col = divmod(wall_idx, maze_width - 1)
            if is_breakable(ids, wall_row, wall_col, wall_type):
                source_id = get_id(a_grid, wall_row, wall_col)
                target_id = get_id(a_grid, wall_row, wall_col + 1)
                a_grid["c_walls"][wall_row][wall_col] = False
                a_grid = rewrite_ids(a_grid, source_id, target_id)
    return a_grid


if __name__ == "__main__":
    start = process_time()
    one_grid = maze(200, 200)
    print_grid_2d(
        one_grid["width"], one_grid["height"], one_grid["c_walls"], one_grid["r_walls"]
    )
    print(f"Time : {process_time() - start} s")
