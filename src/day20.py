import utils
from collections import defaultdict
import copy


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
    # puzzle_input = utils.read_puzzle_input("inputs/day20.txt")
    grid = [list(line) for line in puzzle_input]
    h, w = utils.input_dim(grid)

    start_position = [(i, j) for i in range(h) for j in range(w) if grid[i][j] == "S"][0]
    end_position = [(i, j) for i in range(h) for j in range(w) if grid[i][j] == "E"][0]

    # Get shortest distance without using cheats.
    distances, previous = shortest_path(start=(*start_position, 1), end=end_position, grid=grid, blacklist=set())
    base_distance = distances[(*end_position, 1)]

    print(base_distance)

    # Successively blacklist the cheats encountered and see what's the next best path.
    blacklisted_cheats = set()
    cheated_distances = []
    while True:
        # Find a path while allowing cheating.
        distances, previous = shortest_path(
            start=(*start_position, 0), end=end_position, grid=grid, blacklist=blacklisted_cheats
        )
        cheat_dist = distances[(*end_position, 1)]

        # If this happens, then we couldn't cheat or cheating doesn't help anymore.
        if cheat_dist >= base_distance:
            break

        cheated_distances.append(cheat_dist)

        # Where on the path did we cheat?
        cheat_coordinate = None
        node = previous[(*end_position, 1)]
        while previous[node] is not None:
            if grid[node[0]][node[1]] == "#":
                cheat_coordinate = (node[0], node[1])
                break

            node = previous[node]

        # Because of the distance check above and because we have a singular non-cheat
        # path, this actually shouldn't be possible, so lets assert it to be safe.
        assert cheat_coordinate is not None, "We didn't cheat? Why?"
        blacklisted_cheats.add(cheat_coordinate)
        # print(len(cheated_distances), cheat_dist, base_distance)

    print(f"{len(cheated_distances)} many ways to cheat for benefit.")


def shortest_path(
    start: tuple[int, int, int], end: tuple[int, int], grid: list[list[str]], blacklist: set[tuple[int, int]]
) -> tuple[dict, dict]:
    h, w = utils.input_dim(grid)

    q = utils.PriorityQueue()

    distances = defaultdict(lambda: 100000000000)
    distances[start] = 0

    previous = {start: None}

    q.add_task(start)

    state_stack = []

    while len(q.pq) > 0:
        node = q.pop_task()
        (i, j, cheat_count) = node

        if grid[i][j] == end:
            return distances, previous

        adj_neighbors = [(i + di, j + dj) for (di, dj) in utils.ADJ4 if (i + di) in range(h) and (j + dj) in range(w)]
        neighbors = [(ni, nj, cheat_count) for (ni, nj) in adj_neighbors if grid[ni][nj] != "#"]

        # If we still have a cheat available, we can run into a wall.
        if cheat_count < 1:
            neighbors += [
                (ni, nj, cheat_count + 1)
                for (ni, nj) in adj_neighbors
                if grid[ni][nj] == "#" and (ni, nj) not in blacklist
            ]

        for neighbor in neighbors:
            if distances[neighbor] > distances[node] + 1:
                previous[neighbor] = node
                distances[neighbor] = distances[node] + 1
                q.add_task(neighbor)

    return distances, previous


if __name__ == "__main__":
    main()
