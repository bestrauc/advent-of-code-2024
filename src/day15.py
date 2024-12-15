import numpy as np

import utils

MOVE_MAP = {
    "^": (-1, 0),
    "v": (1, 0),
    "<": (0, -1),
    ">": (0, 1),
}


def main():
    puzzle_input = utils.read_example_input(
        """#######
#...#.#
#.....#
#..OO@#
#..O..#
#.....#
#######

<vv<<^^<<^^"""
    )
    # puzzle_input = utils.read_puzzle_input("inputs/day15_large_example.txt")
    # puzzle_input = utils.read_puzzle_input("inputs/day15.txt")
    grid, moves = utils.split_list_at(puzzle_input, pat="")
    grid = [list(line) for line in grid]
    moves = [c for line in moves for c in line]

    utils.print_grid(grid)

    wide_grid = expand_map(grid)
    utils.print_grid(wide_grid)

    for move in moves:
        print(f"Move {move}:")
        move_robot(grid, move)
        utils.print_grid(grid)
        print()

    utils.print_grid(grid)
    print(box_coordinate_sum(grid))


def move_robot(grid: list[list[str]], direction: str):
    h, w = utils.input_dim(grid)

    di, dj = MOVE_MAP[direction]
    ri, rj = [(i, j) for i in range(h) for j in range(w) if grid[i][j] == "@"][0]
    ni, nj = (ri + di, rj + dj)

    # We'd be moving against a wall -> don't move.
    if grid[ni][nj] == "#":
        return

    def move_boxes(bi: int, bj: int):
        """Recursively move a stack of boxes into the direction we're processing."""
        # There is no box here -> return.
        if grid[bi][bj] != "O":
            return

        b_ni = bi + di
        b_nj = bj + dj

        # Can't move the box into a wall.
        if grid[b_ni][b_nj] == "#":
            return

        # Try to move other boxes out of the way first.
        move_boxes(b_ni, b_nj)

        # Move the box, if it's possible.
        if grid[b_ni][b_nj] == ".":
            grid[b_ni][b_nj] = "O"
            grid[bi][bj] = "."

    # Move boxes, if there are any and we can move them.
    move_boxes(ni, nj)

    # Move the robot if possible
    if grid[ni][nj] == ".":
        grid[ni][nj] = "@"
        grid[ri][rj] = "."


def box_coordinate_sum(grid: list[list[str]]) -> int:
    h, w = utils.input_dim(grid)
    box_positions = [(i, j) for i in range(h) for j in range(w) if grid[i][j] == "O"]
    return sum(100 * i + j for (i, j) in box_positions)


def expand_map(grid: list[list[str]]) -> list[list[str]]:
    new_grid = []
    h, w = utils.input_dim(grid)
    for i in range(h):
        line = []
        for j in range(w):
            if grid[i][j] == "O":
                line.append("[")
                line.append("]")
            elif grid[i][j] == "@":
                line.append("@")
                line.append(".")
            else:
                line.append(grid[i][j])
                line.append(grid[i][j])

        new_grid.append(line)

    return new_grid


if __name__ == "__main__":
    main()
