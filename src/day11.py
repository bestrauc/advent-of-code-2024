import functools
import math
from collections import defaultdict

import utils


def main():
    puzzle_input = utils.read_example_input("""125 17""")[0]
    puzzle_input = utils.read_puzzle_input("inputs/day11.txt")[0]
    nums = utils.nums(puzzle_input)

    # Read a very slight hint about "the order not mattering", which I
    # hadn't considered in my previous brute force. In any case, I'm stupid.
    stone_count = {n: 1 for n in nums}

    for _ in range(75):
        next_counts = defaultdict(int)
        for stone in list(stone_count.keys()):
            for next_stone in evolve_num(stone):
                next_counts[next_stone] += stone_count[stone]

        stone_count = next_counts

    print(sum(stone_count.values()))


@functools.cache
def evolve_num(num: int) -> tuple[int, int]:
    if num == 0:
        return (1,)

    digits = int(math.log10(num)) + 1
    if digits % 2 == 0:
        num1, num2 = divmod(num, 10 ** (digits // 2))
        return num1, num2

    return (num * 2024,)


if __name__ == "__main__":
    main()
