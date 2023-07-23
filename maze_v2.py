from random import randint
from time import process_time

import print_maze as pm


def generate_grid(width, height):
    """Generate a grid and the walls for of the maze

    Args:
        width (int): width of the maze
        height (int): height of the maze

    Returns:
        dict: a dict of the cells ids, the walls, the height and the width of the maze
    """
    return {
        "height": height,
        "width": width,
        "cell_ids": list(range(width * height)),
        "horizontal_walls": [True for _ in range((height - 1) * width)],
        "vertical_walls": [True for _ in range(height * (width - 1))],
    }


def get_cell_id(maze_grid, width, line, column):
    """compute the id of a cell based on her line and column

    Args:
        maze_grid (dict): grid of the maze
        width (int): width of the maze
        line (int): line of the wall
        column (int): column of the wall

    Returns:
        int: id of the cell
    """
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
        cells_ids = my_grid["cell_ids"]
        random_wall = selectable_walls[randint(0, len(selectable_walls) - 1)].split("_")
        wall_type = random_wall[0]
        wall_id = int(random_wall[1])
        if wall_type == "v":
            wall_line = wall_id // (maze_width - 1)
            wall_column = wall_id - wall_line * (maze_width - 1)
            if is_breakable(my_grid, wall_line, wall_column, "vertical"):
                source_id = cells_ids[wall_line * maze_width + wall_column]
                target_id = cells_ids[wall_line * maze_width + wall_column + 1]
                my_grid["vertical_walls"][wall_id] = False
                my_grid = make_path(
                    my_grid,
                    source_id,
                    target_id,
                )
        else:
            wall_line = wall_id // maze_width
            wall_column = wall_id - wall_line * maze_width
            if is_breakable(my_grid, wall_line, wall_column, "horizontal"):
                source_id = cells_ids[wall_line * maze_width + wall_column]
                target_id = cells_ids[(wall_line + 1) * maze_width + wall_column]
                my_grid["horizontal_walls"][wall_id] = False
                my_grid = make_path(
                    my_grid,
                    source_id,
                    target_id,
                )
        selectable_walls.remove(f"{wall_type}_{wall_id}")
    return my_grid


if __name__ == "__main__":
    start_time = process_time()
    the_grid = maze(100, 100)
    pm.print_grid(
        the_grid["width"],
        the_grid["height"],
        the_grid["vertical_walls"],
        the_grid["horizontal_walls"],
    )
    print(f"Time : {process_time() - start_time} s")
