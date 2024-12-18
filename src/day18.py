from collections import defaultdict

from tqdm import tqdm

import utils


def main():
    puzzle_input = utils.read_puzzle_input("inputs/day18.txt")
    byte_positions = [utils.nums(line) for line in puzzle_input]
    print(len(byte_positions))

    dim = max(max(position) for position in byte_positions) + 1
    grid = [["." for i in range(dim)] for j in range(dim)]

    end_position = (dim - 1, dim - 1)
    for j, i in tqdm(byte_positions):
        grid[i][j] = "#"

        distances, previous = shortest_path(start=(0, 0), grid=grid)
        if end_position not in distances:
            print(f"{(j,i)} is preventing a path")
            break


def shortest_path(start: tuple[int, int], grid: list[list[str]]) -> tuple[dict, dict]:
    h, w = utils.input_dim(grid)

    q = utils.PriorityQueue()

    distances = defaultdict(lambda: 100000000000)
    distances[start] = 0

    previous = {start: None}

    q.add_task(start)

    while len(q.pq) > 0:
        node = q.pop_task()
        (i, j) = node

        neighbors = [(i + di, j + dj) for (di, dj) in utils.ADJ4]
        neighbors = [
            (ni, nj)
            for (ni, nj) in neighbors
            # Must be within the grid and a free space.
            if (ni in range(h)) and (nj in range(w)) and grid[i][j] == "."
        ]

        for neighbor in neighbors:
            if distances[neighbor] > distances[node] + 1:
                previous[neighbor] = node
                distances[neighbor] = distances[node] + 1
                q.add_task(neighbor)

    return distances, previous


if __name__ == "__main__":
    main()
