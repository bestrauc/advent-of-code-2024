import utils


def main():
    puzzle_input = utils.read_example_input(
        """....#.....
#........#
..........
..#.......
.......#..
..........
.#..^.....
........#.
#.........
......#..."""
    )
    puzzle_input = utils.read_puzzle_input("inputs/day6.txt")

    puzzle_input = [list(line) for line in puzzle_input]

    trace_path(puzzle_input)


CHAR_TO_DIRECTION = {"^": (-1, 0), "<": (0, -1), ">": (0, 1), "v": (1, 0)}
DIRECTION_TO_CHAR = {v: k for k, v in CHAR_TO_DIRECTION.items()}


def trace_path(grid: list[list[str]]):
    h, w = utils.input_dim(grid)

    pos = [(i, j) for i in range(h) for j in range(w) if grid[i][j] in "<>^v"][0]
    direction = CHAR_TO_DIRECTION[grid[pos[0]][pos[1]]]

    obstacles = [(i, j) for i in range(h) for j in range(w) if grid[i][j] == "#"]
    obstacles = sorted(obstacles)  # Sorted by rows and, within rows, by columns.

    while direction is not None:
        pos, direction = next_guard_position(grid=grid, obstacles=obstacles, pos=pos, direction=direction)

    visited = len([(i, j) for i in range(h) for j in range(w) if grid[i][j] == "X"])
    print(visited)


def next_guard_position(
    grid: list[list[str]],
    obstacles: list[tuple[int, int]],
    pos: tuple[int, int],
    direction: tuple[int, int] | None,
) -> tuple[tuple[int, int], tuple[int, int]]:
    h, w = utils.input_dim(grid)
    y, x = pos
    dy, dx = direction

    # Is here an obstacle in the direction we want to go to?
    # If there is no obstacle, we insert one as an out-of-bounds marker.
    match (dy, dx):
        case (-1, 0):
            next_collisions = [(i, j) for (i, j) in obstacles if (i < y) and (x == j)] + [(-1, x)]
            next_collisions = sorted(next_collisions, reverse=True)  # Want largest row first.
        case (1, 0):
            next_collisions = [(i, j) for (i, j) in obstacles if (i > y) and (x == j)] + [(h, x)]
        case (0, -1):
            next_collisions = [(i, j) for (i, j) in obstacles if (i == y) and (j < x)] + [(y, -1)]
            next_collisions = sorted(next_collisions, reverse=True)  # Want largest col first.
        case (0, 1):
            next_collisions = [(i, j) for (i, j) in obstacles if (i == y) and (j > x)] + [(y, w)]

    # Our next position is one step before we would have collided with the obstacle.
    collision_y, collision_x = next_collisions[0]
    (next_y, next_x) = (collision_y - dy), (collision_x - dx)

    # Note down visited positions for counting & debugging.
    while (y, x) != (next_y, next_x):
        assert grid[y][x] != "#"

        grid[y][x] = "X"
        y += direction[0]
        x += direction[1]

    # If we walked out of bounds, indicate with new direction None.
    if (collision_y, collision_x) not in obstacles:
        grid[next_y][next_x] = "X"
        return (next_y, next_x), None

    next_direction = direction[1], -direction[0]
    grid[y][x] = DIRECTION_TO_CHAR[next_direction]

    return (next_y, next_x), next_direction


if __name__ == "__main__":
    main()
