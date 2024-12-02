import utils
from operator import le, ge

input = utils.read_example_input(
    """7 6 4 2 1
1 2 7 8 9
9 7 6 2 1
1 3 2 4 5
8 6 4 4 1
1 3 6 7 9"""
)
input = utils.read_puzzle_input("inputs/day2.txt")

reports = [utils.nums(line) for line in input]


def is_valid(report: list[int], dampen: bool = False) -> bool:
    op = le if report[0] < report[1] else ge

    for i, (x, y) in enumerate(zip(report, report[1:])):
        if not (op(x, y) and (1 <= abs(x - y) <= 3)):
            if dampen:
                # If (x, y) failed, try removing x or y
                new_str1 = report[: i + 1] + report[i + 2 :]
                new_str2 = report[:i] + report[i + 1 :]

                return is_valid(new_str1, dampen=False) or is_valid(new_str2, dampen=False)

            return False

    return True


part1_safe_reports = 0
for r in reports:
    part1_safe_reports += int(is_valid(r))

print(part1_safe_reports)


part2_safe_reports = 0
for r in reports:
    # My function doens't cover removing the first element, so we manually deal with it.
    is_safe = is_valid(r[1:]) or is_valid(r, dampen=True)
    part2_safe_reports += int(is_safe)

print(part2_safe_reports)
