from collections import defaultdict

import utils


def main():
    puzzle_input = utils.read_example_input(
        """###############
#.......#....E#
#.#.###.#.###.#
#.....#.#...#.#
#.###.#####.#.#
#.#.#.......#.#
#.#.#####.###.#
#...........#.#
###.#.#####.#.#
#...#.....#.#.#
#.#.#.###.#.#.#
#.....#...#.#.#
#.###.#.#.#.#.#
#S..#.....#...#
###############"""
    )
    puzzle_input = utils.read_puzzle_input("inputs/day16.txt")
    grid = [list(line) for line in puzzle_input]

    h, w = utils.input_dim(grid)

    start_position = [(i, j) for i in range(h) for j in range(w) if grid[i][j] == "S"][0]
    start_node = (*start_position, 0, 1)  # We start facing the east.

    distances, previous = shortest_path(start=start_node, grid=grid)

    # Reconstruct the end path!
    end_position = [(i, j) for i in range(h) for j in range(w) if grid[i][j] == "E"][0]
    possible_end_arrivals = [(k, d) for k, d in distances.items() if k[:2] == end_position]
    min_end_position, end_distance = min(possible_end_arrivals, key=lambda kd: kd[1])

    # Traverse our paths and visualize them in the grid.
    def mark_path(node):
        ni, nj, _, _ = node
        grid[ni][nj] = "O"

        for predecessor in previous[node]:
            mark_path(predecessor)

    mark_path(min_end_position)
    on_best_path = len([(i, j) for i in range(h) for j in range(w) if grid[i][j] == "O"])

    utils.print_grid(grid)

    print(f"Reached end with distance {end_distance}, on best path: {on_best_path}")


def shortest_path(start: tuple[int, int, int, int], grid: list[list[str]]):
    """We do a shortest path, with the graph consisting of turns and straight lines.

    Nodes are therefore our position and the direction we're facing in.
    """
    q = utils.PriorityQueue()

    distances = defaultdict(lambda: 100000000000)
    distances[start] = 0

    previous = {start: []}

    q.add_task(start)

    while len(q.pq) > 0:
        node = q.pop_task()
        (ni, nj, di, dj) = node

        # We have i) left turn, ii) right turn as graph neighbors, at a cost of 1000..
        rot_counter = (ni, nj, -dj, di)
        rot_clockwise = (ni, nj, dj, -di)
        neighbors = [(rot_clockwise, 1000), (rot_counter, 1000)]

        # ..and maybe going forward, at a smaller cost, if there's not an obstacle.
        mi = ni + di
        mj = nj + dj
        if grid[mi][mj] != "#":
            forward = (mi, mj, di, dj)
            neighbors.append((forward, 1))

        for neighbor, cost in neighbors:
            new_dist = distances[node] + cost
            if distances[neighbor] >= new_dist:
                # If this is an equivalent path, add this as another path option.
                if distances[neighbor] == new_dist:
                    previous[neighbor] = previous[neighbor] + [node]
                # Otherwise we are strictly superior and only keep the one predecessor.
                else:
                    previous[neighbor] = [node]

                distances[neighbor] = new_dist
                q.add_task(neighbor)

    return distances, previous


if __name__ == "__main__":
    main()
