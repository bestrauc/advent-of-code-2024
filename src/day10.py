import utils


def main():
    puzzle_input = utils.read_example_input(
        """89010123
78121874
87430965
96549874
45678903
32019012
01329801
10456732"""
    )
    puzzle_input = utils.read_puzzle_input("inputs/day10.txt")
    puzzle_input = [[int(n) for n in line] for line in puzzle_input]
    h, w = utils.input_dim(puzzle_input)

    zero_positions = [(i, j) for i in range(h) for j in range(w) if puzzle_input[i][j] == 0]
    print(zero_positions)

    trail_score_sum = 0
    for start in zero_positions:
        trail_score, _ = dfs(grid=puzzle_input, start=start)
        trail_score_sum += trail_score

    print(trail_score_sum)


def dfs(grid: list[list[int]], start: tuple[int, int], visited: list[list[bool]] = None):
    h, w = utils.input_dim(grid)

    if visited is None:
        visited = [[False for i in range(h)] for j in range(w)]

    si, sj = start

    start_height = grid[si][sj]

    # Reached a trailhead.
    if start_height == 9:
        return 1, visited

    trail_sum = 0
    for di, dj in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        ni, nj = (si + di, sj + dj)

        if not ((ni in range(h)) and (nj in range(w))):
            continue

        # Comment this in for part1, comment out for part 2.
        # if visited[ni][nj]:
        #     continue

        n_height = grid[ni][nj]
        if start_height + 1 != n_height:
            continue

        visited[ni][nj] = True

        trail_score, visited = dfs(grid, start=(ni, nj), visited=visited)
        trail_sum += trail_score

    return trail_sum, visited


if __name__ == "__main__":
    main()
