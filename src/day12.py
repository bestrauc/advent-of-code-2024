import itertools
from collections import defaultdict

import numpy as np

# Using well-known data structures is fine I think?
from scipy.cluster.hierarchy import DisjointSet
from termcolor import cprint

import utils


def main():
    puzzle_input = utils.read_example_input(
        """RRRRIICCFF
RRRRIICCCF
VVRRRCCFFF
VVRCCCJFFF
VVVVCJJCFE
VVIVCCJJEE
VVIIICJJEE
MIIIIIJJEE
MIIISIJEEE
MMMISSJEEE"""
    )
    puzzle_input = utils.read_puzzle_input("inputs/day12.txt")
    grid = [[c for c in line] for line in puzzle_input]

    h, w = utils.input_dim(grid)

    components = DisjointSet([(i, j) for i in range(h) for j in range(w)])
    boundaries = defaultdict(set)

    for i in range(h):
        for j in range(w):
            for di, dj in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                ni, nj = i + di, j + dj

                # Skip out of bounds indices, but record them as boundaries.
                if not (ni in range(h) and nj in range(w)):
                    boundaries[components[(i, j)]].add((ni, nj, di, dj))
                    continue

                if grid[i][j] == grid[ni][nj]:
                    root1 = components[(i, j)]
                    root2 = components[(ni, nj)]

                    components.merge((i, j), (ni, nj))
                    root_after = components[(i, j)]

                    # We also have to merge the boundaries, depending on which component got merged into which.
                    # It can also be that root1 == root2 == root_after, so we have two different if checks here.
                    if root1 != root_after:
                        for b in boundaries[root1]:
                            boundaries[root_after].add(b)
                        del boundaries[root1]

                    if root2 != root_after:
                        for b in boundaries[root2]:
                            boundaries[root_after].add(b)
                        del boundaries[root2]
                else:
                    boundaries[components[(i, j)]].add((ni, nj, di, dj))

    sum = 0
    sum_bulk = 0
    for subset in components.subsets():
        root_i, root_j = components[list(subset)[0]]
        component_boundaries = boundaries[components[(root_i, root_j)]]
        label = grid[root_i][root_j]

        area = len(subset)
        perimeter = len(component_boundaries)
        total = area * perimeter

        bulk_perimeter = count_bulk_boundaries(component_boundaries)
        total_bulk = area * bulk_perimeter

        print(
            f"{label}: Area {area}, Perimeter {perimeter}, Total {total}, "
            f"Perimeter (bulk) {bulk_perimeter}, Total (bulk) {total_bulk}"
        )

        sum += total
        sum_bulk += total_bulk

    print(sum)
    print(sum_bulk)

    visualize_components_in_grid(grid, components)


def count_bulk_boundaries(boundaries: set[tuple[int, int, int, int]]) -> int:
    """Given the cell level boundaries, count horizontal/vertical runs of them."""

    count = 0
    for di, dj in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        dir_boundaries = [(b[0], b[1]) for b in boundaries if (b[2], b[3]) == (di, dj)]

        # If we are looking at vertical boundaries.
        check_dim = 0 if dj == 0 else 1
        dir_boundaries = sorted(dir_boundaries, key=lambda b: (b[check_dim], b[not check_dim]))
        for _, vals in itertools.groupby(dir_boundaries, key=lambda b: b[check_dim]):
            # This might give something like a run of [1, 2, 4, 5] x coordinates.
            check_vals = [v[not check_dim] for v in vals]

            # This diff will then be [1, 2, 1], indicating that there are two runs.
            count += 1 + (np.diff(check_vals) != 1).sum()

    return count


COLOR_WHEEL = [
    "red",
    "green",
    "yellow",
    "blue",
    "magenta",
    "cyan",
    "white",
    "light_grey",
    "dark_grey",
    "light_red",
    "light_green",
    "light_yellow",
    "light_blue",
    "light_magenta",
    "light_cyan",
]


def visualize_components_in_grid(grid: list[list[str]], components: DisjointSet):
    h, w = utils.input_dim(grid)

    color_cycler = itertools.cycle(COLOR_WHEEL)
    bold_cycler = itertools.cycle([None, ["bold"]])

    component_color_map = defaultdict(lambda: next(color_cycler))
    bold_map = defaultdict(lambda: next(bold_cycler))

    for i in range(h):
        for j in range(w):
            root = components[(i, j)]
            cprint(grid[i][j], color=component_color_map[root], attrs=bold_map[root], end="")
        print()


if __name__ == "__main__":
    main()
