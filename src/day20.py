from collections import defaultdict

from tqdm import tqdm

import utils


def main():
    puzzle_input = utils.read_example_input(
        """###############
#...#...#.....#
#.#.#.#.#.###.#
#S#...#.#.#...#
#######.#.#.###
#######.#.#...#
#######.#.###.#
###..E#...#...#
###.#######.###
#...###...#...#
#.#####.#.###.#
#.#...#.#.#...#
#.#.#.#.#.#.###
#...#...#...###
###############"""
    )
    puzzle_input = utils.read_puzzle_input("inputs/day20.txt")
    grid = [list(line) for line in puzzle_input]
    h, w = utils.input_dim(grid)

    start_position = [(i, j) for i in range(h) for j in range(w) if grid[i][j] == "S"][0]
    end_position = [(i, j) for i in range(h) for j in range(w) if grid[i][j] == "E"][0]
    path_positions = [(i, j) for i in range(h) for j in range(w) if grid[i][j] != "#"]

    distances_from_start, _ = shortest_path(start=start_position, grid=grid, cheat_dist=None)
    distances_from_end, _ = shortest_path(start=end_position, grid=grid, cheat_dist=None)
    baseline_distance = distances_from_start[end_position]

    assert all([p in distances_from_start for p in path_positions])
    sorted_path = sorted(path_positions, key=lambda n: distances_from_start[n])

    print(baseline_distance)

    # Walk the normal path and from each position, try to cheat within our given
    # cheat time and see if that connects us forward onto the normal path.
    shortcut_count = defaultdict(int)
    for i, path_pos in tqdm(enumerate(sorted_path), total=len(sorted_path)):
        start_to_pos = distances_from_start[path_pos]
        distances_from_path, _ = shortest_path(start=path_pos, grid=grid, cheat_dist=20)
        for shortcut_target in sorted_path[i:]:
            if shortcut_target in distances_from_path:
                shortcut_distance = distances_from_path[shortcut_target]
                shortcut_to_end = distances_from_end[shortcut_target]
                total_dist = start_to_pos + shortcut_distance + shortcut_to_end

                savings = baseline_distance - total_dist

                if savings >= 100:
                    shortcut_count[savings] += 1

    print(sum(shortcut_count.values()))


def shortest_path(start: tuple[int, int, int, int], grid: list[list[str]], cheat_dist: int | None) -> tuple[dict, dict]:
    h, w = utils.input_dim(grid)

    q = utils.PriorityQueue()

    distances = defaultdict(lambda: 100000000000)
    distances[start] = 0

    previous = {start: None}

    q.add_task(start)

    while len(q.pq) > 0:
        node = q.pop_task()
        (i, j) = node

        # If we are in cheat mode, we only explore as many steps as we are allowed.
        if (cheat_dist is not None) and distances[node] == cheat_dist:
            continue

        adj_neighbors = [(i + di, j + dj) for (di, dj) in utils.ADJ4 if (i + di) in range(h) and (j + dj) in range(w)]
        neighbors = [
            (ni, nj)
            for (ni, nj) in adj_neighbors
            # If we are cheating we don't care about boundaries.
            if (cheat_dist is not None and cheat_dist > 0) or (grid[ni][nj] != "#")
        ]

        for neighbor in neighbors:
            if distances[neighbor] > distances[node] + 1:
                previous[neighbor] = node
                distances[neighbor] = distances[node] + 1
                q.add_task(neighbor)

    return distances, previous


if __name__ == "__main__":
    main()
