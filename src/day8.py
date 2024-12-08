import itertools
from collections import defaultdict

import utils


def main():
    puzzle_input = utils.read_example_input(
        """............
........0...
.....0......
.......0....
....0.......
......A.....
............
............
........A...
.........A..
............
............"""
    )
    puzzle_input = utils.read_puzzle_input("inputs/day8.txt")
    puzzle_input = list(map(list, puzzle_input))

    h, w = utils.input_dim(puzzle_input)
    antenna_coords = defaultdict(list)
    for i in range(h):
        for j in range(w):
            char = puzzle_input[i][j]
            if char != ".":
                antenna_coords[char].append((i, j))

    antinode_positions = set()
    for coords in antenna_coords.values():
        # antinodes = compute_antinodes1(coords)
        antinodes = compute_antinodes2(coords, height=h, width=w)
        for y, x in antinodes:
            if y in range(h) and x in range(w):
                antinode_positions.add((y, x))

                if puzzle_input[y][x] == ".":
                    puzzle_input[y][x] = "#"

    print(len(antinode_positions))


def compute_antinodes1(coords: list[tuple[int, int]]) -> list:
    """For all pairs of points, get the antinodes where one is twice as far away as the other.

    With how part2 turned out to test all grid positions anyway, this was probably overkill.
    """

    antinodes = []
    for (y1, x1), (y2, x2) in itertools.combinations(coords, 2):
        # Entered roughly these equation into Wolfram Alpha to arrive at the solutions:
        # - define PA(t) = P1 + t(P2 - P1)
        # - solve d(PA(t), P1) = 2*d(PA(t), P2)
        # - solve 2*d(PA(t), P1) = d(PA(t), P2)
        # In the solver, I wrote in terms of y(t), x(t) and actually wrote down the
        # distances as d(PA(t), P1) = sqrt((y(t) - y1)^2 + (x(t) - x1)^2) and so on.
        for t in [-1, 1 / 3, 2 / 3, 2]:
            ynew = y1 + t * (y2 - y1)
            xnew = x1 + t * (x2 - x1)

            if float(ynew).is_integer() and float(xnew).is_integer():
                antinodes.append((int(ynew), int(xnew)))

    return antinodes


def compute_antinodes2(coords: list[tuple[int, int]], height: int, width: int) -> list:
    """For all pairs of points, get the grid positions that are in line with them."""
    antinodes = []
    for (y1, x1), (y2, x2) in itertools.combinations(coords, 2):
        for y in range(height):
            for x in range(width):
                if _is_on_line(y, x, x1, y1, x2, y2):
                    antinodes.append((y, x))

    return antinodes


def _is_on_line(y_test: int, x_test: int, x1: int, y1: int, x2: int, y2: int) -> bool:
    """Check if (x_test, y_test) is on the line defined by (x1, y1) and (x2, y2)."""
    return (x_test - x1) * (y2 - y1) == (y_test - y1) * (x2 - x1)


if __name__ == "__main__":
    main()
