import re
import utils

puzzle_input = utils.read_example_input("""xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))""")
puzzle_input = utils.read_example_input("""xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))""")
puzzle_input = utils.read_puzzle_input("inputs/day3.txt")
puzzle_input = "".join(puzzle_input)

INSTRUCTION_REGEX = r"mul\((\d+),(\d+)\)|(do\(\))|(don't\(\))"

sum = 0
active = True

for arg1, arg2, is_do, is_dont in re.findall(INSTRUCTION_REGEX, puzzle_input):
    if is_do != "":
        active = True
    elif is_dont != "":
        active = False
    elif active:
        sum += int(arg1) * int(arg2)

print(sum)
