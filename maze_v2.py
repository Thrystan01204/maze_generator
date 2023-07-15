def generate_grid(width, height):
    return {
        "height": height,
        "width": width,
        "cell_ids": list(range(width * height)),
        "horizontal_walls": [True for _ in range((height - 1) * width)],
        "vertical_walls": [True for _ in range(height * (width - 1))],
    }


def get_cell_id(labyrinth_grid, width, line, column):
    return labyrinth_grid["cell_ids"][width * line + column]


def is_breakable(maze_grid, wall_line, wall_column, wall_type):
    # Dépassemnt de la hauteur max des murs cassables
    if wall_type == "horizontal" and wall_line > maze_grid["cell_ids"] - 2:
        return False
    # Dépassemnt de la largeur max des murs cassables
    if wall_type == "vertical" and wall_column > maze_grid["cell_ids"] - 2:
        return False
    # Horizontal wall with a cell below with the same ID as current
    if wall_type == "horizontal" and get_cell_id(
        maze_grid, maze_grid["width"], wall_line, wall_column
    ) == get_cell_id(maze_grid, maze_grid["width"], wall_line + 1, wall_column):
        return False
    # Vertical wall with a cell at right with same ID as current
    if wall_type == "vertical" and get_cell_id(
        maze_grid, maze_grid["width"], wall_line, wall_column
    ) == get_cell_id(maze_grid, maze_grid["width"], wall_line, wall_column + 1):
        return False
    return True


def main(maze_width, maze_height):
    my_grid = generate_grid(maze_height, maze_width)
