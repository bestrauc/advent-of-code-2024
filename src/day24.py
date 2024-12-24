import functools
import operator

import utils

GATE_OPS = {
    "AND": operator.and_,
    "OR": operator.or_,
    "XOR": operator.xor,
}


def main():
    puzzle_input = utils.read_example_input(
        """x00: 1
x01: 1
x02: 1
y00: 0
y01: 1
y02: 0

x00 AND y00 -> z00
x01 XOR y01 -> z01
x02 OR y02 -> z02"""
    )
    # Note: I sorted the rules in the input, which doesn't change anything but visually groups the xs and ys.
    puzzle_input = utils.read_puzzle_input("inputs/day24.txt")

    inputs, rules = utils.split_list_at(puzzle_input, pat="")

    # Dict from the "x00: 1" lines -> {"x00": "1"}, then convert to int -> {"x00": 1}
    initial_gate_values = dict([line.split(": ") for line in inputs])
    initial_gate_values = {k: int(v) for k, v in initial_gate_values.items()}

    # Parse the rules
    parsed_rules = dict()

    for i, rule in enumerate(rules):
        rule_input, output = rule.split(" -> ")
        l_arg, op, r_arg = rule_input.split(" ")
        parsed_rules[(l_arg, op, r_arg)] = output

        # Print the graph to visualize it in GraphViz for part 2.
        print(f"{l_arg} -> {op}{i};")
        print(f"{r_arg} -> {op}{i};")
        print(f"{op}{i} -> {output};")
    print()

    part1_result = compute_result(parsed_rules, initial_gate_values)
    print(f"Part 1: {part1_result}")
    print()

    # For part 2, I test through all adders independently. Bits x_i and y_i
    # should result in in an output with z_i = x_i + y_i. For starters, I ignored
    # carry effects and only tested (0, 1) and (1, 0), which was sufficient for
    # my input. This locates four corrupted adders, which I then simply checked out
    # in the GraphViz visualization, where it was easy to find the respective swaps.
    zero_gates = {}
    for i in range(45):
        zero_gates[f"x{i:02d}"] = 0
        zero_gates[f"y{i:02d}"] = 0

    print("Testing through the 45 adders")
    for i in range(45):
        test_gates = dict(zero_gates)
        for xbit, ybit in [(0, 1), (1, 0)]:
            test_gates[f"x{i:02d}"] = xbit
            test_gates[f"y{i:02d}"] = ybit
            test_result = compute_result(parsed_rules, test_gates)
            expected_result = (xbit + ybit) << i

            if test_result != expected_result:
                print(f"z{i:02d} {(xbit, ybit)}:    {expected_result} {test_result}")

    # These I noted down as I fixed them for the adders, in my case z15, z20, z27 and z37.
    flips = ["z15", "qnw", "cqr", "z20", "nfj", "ncd", "vkg", "z37"]
    print(f"Part 2: {','.join(sorted(flips))}")


def compute_result(parsed_rules: dict, initial_gate_values: dict[int]) -> int:
    gate_values = dict(initial_gate_values)
    parsed_rules = dict(parsed_rules)

    # Part1: Do the naive thing for now: Apply rules until all z-producing rules are
    # gone. We could optimize the application order later with topological sort.
    while any(output.startswith("z") for output in parsed_rules.values()):
        for rule, output in list(parsed_rules.items()):
            l_arg, op, r_arg = rule

            # If we don't have the inputs required for this rule yet, skip.
            if not ((l_arg in gate_values) and (r_arg in gate_values)):
                continue

            assert output not in gate_values, "Output shouldn't be set yet."

            l_val, r_val = gate_values[l_arg], gate_values[r_arg]
            gate_values[output] = GATE_OPS[op](l_val, r_val)
            del parsed_rules[rule]

    z_outputs = {k: v for k, v in gate_values.items() if k.startswith("z")}

    # Ordered as z_n, z_{n-1}, .., z_0, from most to least significant bit.
    z_ordered = [z_outputs[k] for k in sorted(z_outputs.keys(), reverse=True)]
    z_value = functools.reduce(lambda acc, bit: (acc << 1) | bit, z_ordered, 0)
    return z_value


if __name__ == "__main__":
    main()
