from random import shuffle
from time import process_time

from print_maze import print_grid


def gen_grid(width, height):
    return {
        "ids": list(range(width * height)),
        "r_walls": [True for _ in range(width * (height - 1))],
        "c_walls": [True for _ in range((width - 1) * height)],
        "width": width,
        "height": height,
    }


def get_id(ids, width, row, col):
    return ids[width * row + col]


def is_breakable(maze_grid, wall_row, wall_col, wall_type):
    ids = maze_grid["ids"]
    width = maze_grid["width"]
    if wall_type == "r":
        if get_id(ids, width, wall_row, wall_col) == get_id(
            ids, width, wall_row + 1, wall_col
        ):
            return False
    if wall_type == "c":
        if get_id(ids, width, wall_row, wall_col) == get_id(
            ids, width, wall_row, wall_col + 1
        ):
            return False
    return True


def rewrite_ids(maze_grid, source_id, target_id):
    new_ids = [
        source_id if cell_id == target_id else cell_id for cell_id in maze_grid["ids"]
    ]
    maze_grid["ids"] = new_ids
    return maze_grid


def all_walls(r_walls, c_walls):
    walls = []
    for wall in range(len(r_walls)):
        walls.append(f"r{wall}")
    for wall in range(len(c_walls)):
        walls.append(f"c{wall}")
    return walls


def maze(maze_width, maze_height):
    maze_grid = gen_grid(maze_width, maze_height)
    walls = all_walls(maze_grid["r_walls"], maze_grid["c_walls"])
    shuffle(walls)

    for wall in walls:
        wall_type = wall[0]
        wall_idx = int(wall[1:])
        if wall_type == "r":
            wall_row, wall_col = divmod(wall_idx, maze_width)
            ids = maze_grid["ids"]
            if is_breakable(maze_grid, wall_row, wall_col, "r"):
                source_id = get_id(ids, maze_width, wall_row, wall_col)
                target_id = get_id(ids, maze_width, wall_row + 1, wall_col)
                maze_grid["r_walls"][wall_idx] = False
                maze_grid = rewrite_ids(maze_grid, source_id, target_id)
        else:
            wall_row, wall_col = divmod(wall_idx, maze_width - 1)
            ids = maze_grid["ids"]
            if is_breakable(maze_grid, wall_row, wall_col, "c"):
                source_id = get_id(ids, maze_width, wall_row, wall_col)
                target_id = get_id(ids, maze_width, wall_row, wall_col + 1)
                maze_grid["c_walls"][wall_idx] = False
                maze_grid = rewrite_ids(maze_grid, source_id, target_id)

    return maze_grid


if __name__ == "__main__":
    start = process_time()
    grid = maze(200, 200)
    print_grid(grid["width"], grid["height"], grid["c_walls"], grid["r_walls"])
    print(f"Time : {process_time() - start} s")
