import utils


def main():
    puzzle_input = utils.read_example_input(
        """190: 10 19
3267: 81 40 27
83: 17 5
156: 15 6
7290: 6 8 6 15
161011: 16 10 13
192: 17 8 14
21037: 9 7 18 13
292: 11 6 16 20"""
    )
    puzzle_input = utils.read_puzzle_input("inputs/day7.txt")
    puzzle_input = [utils.nums(line) for line in puzzle_input]

    sum = 0
    for test_value, *nums in puzzle_input:
        operator_results = generate_operator_combinations(nums)

        possible_operators = {k: v for k, v in operator_results.items() if v == test_value}
        if len(possible_operators) > 0:
            print(f"{test_value}: {nums} possible via {list(possible_operators.keys())}")
            sum += test_value

    print(sum)


def generate_operator_combinations(nums: list[int]) -> dict:
    """Generate the various combinations to check if one of them succeeds.

    Somehow found this easier than a straight recursion for tracking the operator
    chains, which aren't necessary in of themselves, but useful for debugging.
    """

    n = len(nums)
    sub_problems = {0: {"": nums[0]}}

    for k in range(1, n):
        sub_problems[k] = dict()
        for op_history, sub_result in sub_problems[k - 1].items():
            sub_problems[k][op_history + "+"] = sub_result + nums[k]
            sub_problems[k][op_history + "*"] = sub_result * nums[k]
            sub_problems[k][op_history + "||"] = int(str(sub_result) + str(nums[k]))

    return sub_problems[n - 1]


if __name__ == "__main__":
    main()
