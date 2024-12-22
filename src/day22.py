import utils
import numpy as np
from collections import Counter
from collections import defaultdict


PRUNE_MOD = 2**24 - 1


def main():
    puzzle_input = utils.read_example_input(
        """1
2
3
2024"""
    )
    puzzle_input = utils.read_puzzle_input("inputs/day22.txt")
    nums = [int(line) for line in puzzle_input]

    result_sum = 0
    result_digits = []
    for num in nums:
        result = num
        digits = [result % 10]
        for _ in range(2000):
            result = evolve_number(result)
            digits.append(result % 10)

        result_sum += result
        result_digits.append(digits)

    x = np.array(result_digits)
    xd = np.diff(x, axis=1)

    # For all diffs in all rows, get the scores the first time they occur
    # and accumnulate them. Then we'll have a score sum for each diff sequence.
    window_scores = defaultdict(int)
    for i, row in enumerate(xd):
        seen = set()
        diff_windows = np.lib.stride_tricks.sliding_window_view(row, window_shape=4)
        for j, window in enumerate(diff_windows):
            win_key = tuple(window.tolist())
            if win_key in seen:
                continue

            window_scores[win_key] += x[i, j + 4]
            seen.add(win_key)

    print(result_sum, max(window_scores.items(), key=lambda kv: kv[1]))


def evolve_number(num: int) -> int:
    num = (num ^ (num << 6)) & PRUNE_MOD
    num = (num ^ (num >> 5)) & PRUNE_MOD
    num = (num ^ (num << 11)) & PRUNE_MOD
    return num


if __name__ == "__main__":
    main()
