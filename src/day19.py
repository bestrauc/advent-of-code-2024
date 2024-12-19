import functools

import utils


def main():
    puzzle_input = utils.read_example_input(
        """r, wr, b, g, bwu, rb, gb, br

brwrr
bggr
gbbr
rrbgbr
ubwu
bwurrg
brgr
bbrgwb"""
    )
    puzzle_input = utils.read_puzzle_input("inputs/day19.txt")
    patterns, designs = utils.split_list_at(puzzle_input, pat="")
    patterns = tuple([pat.strip() for pat in patterns[0].split(",")])

    arragement_counts = [count_feasible_arrangements(design, patterns) for design in designs]

    # Part 1
    print(sum([c > 0 for c in arragement_counts]))

    # Part 2
    print(sum([c for c in arragement_counts]))


@functools.cache
def count_feasible_arrangements(design: str, patterns: tuple[str]) -> bool:
    """Recursively generate the design by matching patterns.

    The cache is important to memoize the shared subproblems.
    """
    if len(design) == 0:
        return 1

    feasible = 0
    for pat in patterns:
        n = len(pat)
        if design[:n] == pat:
            feasible += count_feasible_arrangements(design[n:], patterns)

    return feasible


if __name__ == "__main__":
    main()
