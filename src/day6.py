import utils
import copy
from tqdm import tqdm


CHAR_TO_DIRECTION = {"^": (-1, 0), "<": (0, -1), ">": (0, 1), "v": (1, 0)}
DIRECTION_TO_CHAR = {v: k for k, v in CHAR_TO_DIRECTION.items()}


class LoopError(Exception):
    pass


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
    h, w = utils.input_dim(puzzle_input)

    visited = trace_path(puzzle_input)

    # Part 1
    print(len(visited))

    # Part 2: Try replacing all visited positions with an obstacle and count where we get loops.
    # One could probably be smarter about which positions can even induce loops, but..
    start_pos = [(i, j) for i in range(h) for j in range(w) if puzzle_input[i][j] in "<>^v"][0]

    loops = 0
    for py, px in tqdm(visited - {start_pos}):
        modified_input = copy.deepcopy(puzzle_input)
        modified_input[py][px] = "O"

        try:
            visited = trace_path(modified_input)
        except LoopError:
            loops += 1

    print(loops)


def trace_path(puzzle_input: list[list[str]]) -> set[tuple[int, int]]:
    grid = copy.deepcopy(puzzle_input)
    h, w = utils.input_dim(grid)

    pos = [(i, j) for i in range(h) for j in range(w) if grid[i][j] in "<>^v"][0]
    direction = CHAR_TO_DIRECTION[grid[pos[0]][pos[1]]]

    obstacles = [(i, j) for i in range(h) for j in range(w) if grid[i][j] in "#O"]
    obstacles = sorted(obstacles)  # Sorted by rows and, within rows, by columns.

    visit_count_history = []
    visited = set()
    while direction is not None:
        pos, direction, visited = next_guard_position(
            grid=grid,
            obstacles=obstacles,
            pos=pos,
            direction=direction,
            visited_positions=visited,
        )
        visit_count_history.append(len(visited))

        # Stupid, but simple solution to detect loops. Window size 4 to account for rotating on the spot.
        if len(visit_count_history) > 4 and len(set(visit_count_history[-4:])) == 1:
            raise LoopError("Encountered loop")

    return visited


def next_guard_position(
    grid: list[list[str]],
    obstacles: list[tuple[int, int]],
    pos: tuple[int, int],
    direction: tuple[int, int] | None,
    visited_positions: set[tuple[int, int]],
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

    # Note down visited positions in a set.
    while (y, x) != (next_y, next_x):
        assert grid[y][x] != "#"
        visited_positions.add((y, x))
        y += direction[0]
        x += direction[1]

    # If we walked out of bounds, indicate with new direction None.
    if (collision_y, collision_x) not in obstacles:
        visited_positions.add((next_y, next_x))
        return (next_y, next_x), None, visited_positions

    next_direction = direction[1], -direction[0]
    return (next_y, next_x), next_direction, visited_positions


if __name__ == "__main__":
    main()
