from random import randint


def generate_grid(height: int, width: int) -> dict:
    return {
        "cell_ids": list(range(width * height)),
        "in_v_walls": [[True for _ in range(width - 1)] for _ in range(height)],
        "in_h_walls": [[True for _ in range(width)] for _ in range(height - 1)],
        "height": height,
        "width": width,
    }


def get_id(cell_ids: list[int], width: int, line: int, column: int) -> int:
    return cell_ids[width * line + column]


def break_wall(walls: list, line: int, column: int) -> None:
    walls[line][column] = False


def make_path(
    grid: dict,
    source: int,
    target: int,
    cell_ids: str = "cell_ids",
) -> dict:
    grid[cell_ids] = [target if id == source else id for id in grid[cell_ids]]
    return grid


def is_breakable(grid: dict, line: int, column: int, wall: str) -> bool:
    if wall == "bottom" and line > grid["height"] - 2:
        return False
    if wall == "right" and column > grid["width"] - 2:
        return False
    if (
        wall == "bottom"
        and grid["cell_ids"][(line + 1) * grid["width"] + column]
        == grid["cell_ids"][line * grid["width"] + column]
    ):
        return False
    if (
        wall == "right"
        and grid["cell_ids"][line * grid["width"] + (column + 1)]
        == grid["cell_ids"][line * grid["width"] + column]
    ):
        return False
    return True


def maze(grid: dict):
    new_grid = {}
    while len(set(grid["cell_ids"])) != 1:
        random_line = randint(0, grid["height"] - 1)
        random_column = randint(0, grid["width"] - 1)
        random_wall = "bottom" if randint(0, 1) == 0 else "right"
        target = 0
        if is_breakable(grid, random_line, random_column, random_wall):
            if random_wall == "bottom":
                target = get_id(
                    grid["cell_ids"], grid["width"], random_line + 1, random_column
                )
                break_wall(grid["in_h_walls"], random_line, random_column)
            else:
                target = get_id(
                    grid["cell_ids"], grid["width"], random_line, random_column + 1
                )
                break_wall(grid["in_v_walls"], random_line, random_column)
            new_grid = make_path(
                grid,
                get_id(grid["cell_ids"], grid["width"], random_line, random_column),
                target,
            )
    return grid


def print_closed_h_walls(width):
    for j in range(width):
        print("+---", end="")
    print("+")


def print_h_walls(width, line, h_walls):
    for j in range(width):
        if h_walls[line][j]:
            print("+---", end="")
        else:
            print("+   ", end="")
    print("+")


def print_v_walls(width, line, v_walls):
    print("|", end="")
    for j in range(width - 1):
        if v_walls[line][j]:
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


grid = generate_grid(10, 5)
print_grid(grid["width"], grid["height"], grid["in_v_walls"], grid["in_h_walls"])

print("----------------- NEW GRID -----------------")

new_grid = maze(grid)
print_grid(
    new_grid["width"],
    new_grid["height"],
    new_grid["in_v_walls"],
    new_grid["in_h_walls"],
)
