import numpy as np

import utils


def main():
    puzzle_input = utils.read_example_input(
        """p=0,4 v=3,-3
p=6,3 v=-1,-3
p=10,3 v=-1,2
p=2,0 v=2,-1
p=0,0 v=1,3
p=3,0 v=-2,-2
p=7,6 v=-1,-3
p=3,0 v=-1,-2
p=9,3 v=2,3
p=7,3 v=-1,2
p=2,4 v=2,-3
p=9,5 v=-3,-3"""
    )
    h, w = 7, 11

    puzzle_input = utils.read_puzzle_input("inputs/day14.txt")
    h, w = 103, 101

    robots = np.array([utils.nums(line) for line in puzzle_input])

    # Part 1
    moved_robots = move_positions(robots.copy(), h=h, w=w, steps=100)
    counts = count_quadrants(moved_robots, h=h, w=w)
    print(counts)
    print(np.prod(counts))

    # Part 2
    # Two observations:
    # - I noticed all the robots visit each field exactly once before returning
    #   to their start position, so we only have to search up to w*h many steps.
    # - The 101x103 area is big compared to the 500 robots. So if they want to
    #   display a tree, they probably need to gather in one quadrant for that.
    moved_robots = robots.copy()
    for i in range(h * w):
        # Check if 50% of the robots are gathered in one quadrant.
        counts = count_quadrants(moved_robots, h=h, w=w)
        rel_counts = counts / len(robots)

        # Let's hope this is it.
        if (rel_counts > 0.5).any():
            print_robot_state(moved_robots, h=h, w=w)
            print(f"Do you see a tree after {i} seconds?")
            break

        moved_robots = move_positions(moved_robots, h=h, w=w, steps=1)


def move_positions(robots: np.ndarray, h: int, w: int, steps: int) -> np.ndarray:
    robots[:, 0] = (robots[:, 0] + robots[:, 2] * steps) % w
    robots[:, 1] = (robots[:, 1] + robots[:, 3] * steps) % h

    return robots


def count_quadrants(robots: list, h: int, w: int) -> dict:
    quadrant_counts = np.zeros(shape=(2, 2))

    for x, y, _, _ in robots:
        h_half = (h - 1) / 2
        w_half = (w - 1) / 2

        if (x == w_half) or (y == h_half):
            continue

        quadrant_counts[int(y > h_half), int(x > w_half)] += 1

    return quadrant_counts


def print_robot_state(robots: list, h: int, w: int):
    for i in range(h):
        for j in range(w):
            robo_count = len([r for r in robots if (j, i) == (r[0], r[1])])
            if robo_count == 0:
                print(".", end="")
            else:
                print(f"{robo_count}", end="")

        print()


if __name__ == "__main__":
    main()
