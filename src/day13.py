import re

import numpy as np

import utils


def main():
    puzzle_input = utils.read_example_input(
        """Button A: X+94, Y+34
Button B: X+22, Y+67
Prize: X=8400, Y=5400

Button A: X+26, Y+66
Button B: X+67, Y+21
Prize: X=12748, Y=12176

Button A: X+17, Y+86
Button B: X+84, Y+37
Prize: X=7870, Y=6450

Button A: X+69, Y+23
Button B: X+27, Y+71
Prize: X=18641, Y=10279"""
    )
    puzzle_input = utils.read_puzzle_input("inputs/day13.txt")
    puzzle_input = utils.split_list_at(puzzle_input, pat="")
    parsed = [_parse_button(*block) for block in puzzle_input]

    total = 0
    cost = np.array([3, 1])

    for a, b, prize in parsed:
        c = np.array(prize)

        # Part 2:
        c += 10000000000000

        # Used Wolfram Alpha to rearrange the equation, too annoying.
        x = (b[1] * c[0] - b[0] * c[1]) / (b[1] * a[0] - a[1] * b[0])
        y = (a[0] * c[1] - a[1] * c[0]) / (b[1] * a[0] - a[1] * b[0])

        if x.is_integer() and y.is_integer():
            total += sum([x, y] * cost)

    print(int(total))


def _parse_button(button_a: str, button_b: str, prize: str):
    ax, ay = re.findall(r"X\+(?P<x>\d+), Y\+(?P<y>\d+)", button_a)[0]
    bx, by = re.findall(r"X\+(?P<x>\d+), Y\+(?P<y>\d+)", button_b)[0]
    px, py = re.findall(r"X=(?P<x>\d+), Y=(?P<y>\d+)", prize)[0]

    return [
        (int(ax), int(ay)),
        (int(bx), int(by)),
        (int(px), int(py)),
    ]


if __name__ == "__main__":
    main()
