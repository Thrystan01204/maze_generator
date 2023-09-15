from random import seed, shuffle
from time import perf_counter
from timeit import timeit
from typing import List

from dijkstra import dijkstra, get_path
from print_maze import print_grid

# seed(1204)


def gen_grid(width: int, height: int) -> dict:
    return {
        "ids": list(range(width * height)),
        "r_walls": [True for _ in range(width * (height - 1))],
        "c_walls": [True for _ in range((width - 1) * height)],
        "width": width,
        "height": height,
    }


def get_id(ids: List[int], width: int, row: int, col: int) -> int:
    return ids[width * row + col]


def is_breakable(maze_grid: dict, wall_row: int, wall_col: int, wall_type: str) -> bool:
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


def rewrite_ids(maze_grid: dict, source_id: int, target_id: int) -> dict:
    new_ids = [
        source_id if cell_id == target_id else cell_id for cell_id in maze_grid["ids"]
    ]
    maze_grid["ids"] = new_ids
    return maze_grid


def all_walls(r_walls: List[bool], c_walls: List[bool]) -> List[tuple]:
    return [("r", wall_idx) for wall_idx in range(len(r_walls))] + [
        ("c", wall_idx) for wall_idx in range(len(c_walls))
    ]


def maze(maze_width: int, maze_height: int) -> dict:
    maze_grid = gen_grid(maze_width, maze_height)
    walls = all_walls(maze_grid["r_walls"], maze_grid["c_walls"])
    shuffle(walls)

    for wall in walls:
        wall_type, wall_idx = wall
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
    start = perf_counter()
    WIDTH = 10
    HEIGHT = 10
    REP = 1000
    START = 4
    grid = maze(WIDTH, HEIGHT)
    print_grid(grid["width"], grid["height"], grid["c_walls"], grid["r_walls"])
    weights = dijkstra(
        START, grid["r_walls"], grid["c_walls"], grid["width"], grid["height"]
    )
    print(f"{weights = }")
    solution = get_path(
        weights,
        0,
        START,
        grid["c_walls"],
        grid["r_walls"],
        grid["width"],
        grid["height"],
    )
    print(f"{solution = }")
    print(f"Time : {perf_counter() - start:.3f} s")

    timeit_func = "maze(WIDTH,HEIGHT)"
    timeit_setup = "from __main__ import maze;from __main__ import WIDTH; from __main__ import HEIGHT"

    print(
        f"{REP} x maze({WIDTH}, {HEIGHT}) : {timeit(timeit_func, setup=timeit_setup, number=REP)}"
    )
