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


def print_h_walls_2d(width, line, h_walls):
    for j in range(width):
        if h_walls[line][j]:
            print("+---", end="")
        else:
            print("+   ", end="")
    print("+")


def print_v_walls_2d(width, line, v_walls):
    print("|", end="")
    for j in range(width - 1):
        if v_walls[line][j]:
            print("   |", end="")
        else:
            print("    ", end="")
    print("   |")


def print_grid_2d(width, height, v_walls, h_walls):
    print_closed_h_walls(width)
    for i in range(height - 1):
        print_v_walls_2d(width, i, v_walls)
        print_h_walls_2d(width, i, h_walls)
    print_v_walls_2d(width, height - 1, v_walls)
    print_closed_h_walls(width)
