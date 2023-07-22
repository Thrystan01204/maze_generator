from random import randint
from time import process_time

import numpy as np


def print_closed_h_walls(width):
    for _ in range(width):
        print("+---", end="")
    print("+")


def print_h_walls(width, line, h_walls):
    for j in range(width):
        if h_walls[width * line + j]:
            print("+---", end="")
        else:
            print("+   ", end="")
    print("+")


def print_v_walls(width, line, v_walls):
    print("|", end="")
    for j in range(width - 1):
        if v_walls[(width - 1) * line + j]:
            print("   |", end="")
        else:
            print("    ", end="")
    print("   |")


def print_grid(width, height, v_walls, h_walls):
    print_closed_h_walls(width)
    for i in range(height - 1):
        print_v_walls(width, i, v_walls)
        print_h_walls(width, i, h_walls)
    print_v_walls(width, height - 1, v_walls)
    print_closed_h_walls(width)


def generate_grid(width, height):
    return {
        "height": height,
        "width": width,
        "cell_ids": list(range(width * height)),
        "np_cell_ids": np.arange(width * height),
        "horizontal_walls": [True for _ in range((height - 1) * width)],
        "vertical_walls": [True for _ in range(height * (width - 1))],
    }


def get_cell_id(maze_grid, width, line, column):
    return maze_grid["cell_ids"][width * line + column]


def is_breakable(maze_grid, wall_line, wall_column, wall_type):
    # Horizontal wall with a cell below with the same ID as current
    if wall_type == "horizontal":
        if get_cell_id(
            maze_grid, maze_grid["width"], wall_line + 1, wall_column
        ) == get_cell_id(maze_grid, maze_grid["width"], wall_line, wall_column):
            return False
    # Vertical wall with a cell at right with same ID as current
    if wall_type == "vertical":
        # Dépassemnt de la largeur max des murs cassables
        if get_cell_id(
            maze_grid, maze_grid["width"], wall_line, wall_column + 1
        ) == get_cell_id(maze_grid, maze_grid["width"], wall_line, wall_column):
            return False
    return True


def generate_selectable_walls(maze_grid):
    selectable_walls = []
    for wall in range(len(maze_grid["horizontal_walls"])):
        selectable_walls.append(f"h_{wall}")
    for wall in range(len(maze_grid["vertical_walls"])):
        selectable_walls.append(f"v_{wall}")
    return selectable_walls


def make_path(maze_grid, source_id, target_id, ids="cell_ids"):
    maze_grid[ids] = [
        source_id if cell_id == target_id else cell_id for cell_id in maze_grid[ids]
    ]
    return maze_grid


def maze(maze_width, maze_height):
    my_grid = generate_grid(maze_height, maze_width)
    selectable_walls = generate_selectable_walls(my_grid)
    while len(selectable_walls) > 0:
        random_wall = selectable_walls[randint(0, len(selectable_walls) - 1)].split("_")
        wall_type = random_wall[0]
        wall_id = int(random_wall[1])
        if wall_type == "v":
            wall_line = wall_id // (maze_width - 1)
            wall_column = wall_id - wall_line * (maze_width - 1)
            source_id = my_grid["cell_ids"][wall_line * my_grid["width"] + wall_column]
            target_id = my_grid["cell_ids"][
                wall_line * my_grid["width"] + wall_column + 1
            ]
            if is_breakable(my_grid, wall_line, wall_column, "vertical"):
                my_grid["vertical_walls"][wall_id] = False
                my_grid = make_path(
                    my_grid,
                    source_id,
                    target_id,
                )
        else:
            wall_line = wall_id // maze_width
            wall_column = wall_id - wall_line * maze_width
            source_id = my_grid["cell_ids"][wall_line * my_grid["width"] + wall_column]
            target_id = my_grid["cell_ids"][
                (wall_line + 1) * my_grid["width"] + wall_column
            ]
            if is_breakable(my_grid, wall_line, wall_column, "horizontal"):
                my_grid["horizontal_walls"][wall_id] = False
                my_grid = make_path(
                    my_grid,
                    source_id,
                    target_id,
                )
        selectable_walls.remove(f"{random_wall[0]}_{random_wall[1]}")
    return my_grid


start_time = process_time()
the_grid = maze(3, 3)
print_grid(
    the_grid["width"],
    the_grid["height"],
    the_grid["vertical_walls"],
    the_grid["horizontal_walls"],
)
print(f"Time : {process_time() - start_time} s")
