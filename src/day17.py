import math
import utils


class ProgramState:
    def __init__(self, registers: list[int]):
        self.registers = registers

        self.ip = 0
        self.outputs = []

    def run_instructions(self, instructions: list[int]):
        instruction_map = {
            0: self.adv,
            1: self.bxl,
            2: self.bst,
            3: self.jnz,
            4: self.bxc,
            5: self.out,
            6: self.bdv,
            7: self.cdv,
        }

        while self.ip < len(instructions):
            opcode, operand = instructions[self.ip], instructions[self.ip + 1]

            instruction_map[opcode](operand)

    def combo_operand_value(self, operand: int) -> int:
        match operand:
            case num if num in range(0, 4):
                return num
            case num if num in range(4, 7):
                return self.registers[num - 4]
            case num:
                raise AssertionError(f"{num} shouldn't occur")

    def literal_operand_value(self, operand: int) -> int:
        return operand

    def adv(self, operand: int):
        self.registers[0] = self._dv(operand)
        self.ip += 2

    def bdv(self, operand: int):
        self.registers[1] = self._dv(operand)
        self.ip += 2

    def cdv(self, operand: int):
        self.registers[2] = self._dv(operand)
        self.ip += 2

    def _dv(self, operand: int) -> int:
        result = self.registers[0] / math.pow(2, self.combo_operand_value(operand))
        return int(result)

    def bxl(self, operand: int):
        self.registers[1] = self.registers[1] ^ self.literal_operand_value(operand)
        self.ip += 2

    def bst(self, operand: int):
        self.registers[1] = self.combo_operand_value(operand) % 8
        self.ip += 2

    def jnz(self, operand: int):
        if self.registers[0] == 0:
            self.ip += 2
        else:
            self.ip = self.literal_operand_value(operand)

    def bxc(self, operand: int):
        self.registers[1] = self.registers[1] ^ self.registers[2]
        self.ip += 2

    def out(self, operand: int):
        self.outputs.append(self.combo_operand_value(operand) % 8)
        self.ip += 2


def main():
    puzzle_input = utils.read_example_input(
        """Register A: 2024
Register B: 0
Register C: 0

Program: 0,3,5,4,3,0"""
    )
    puzzle_input = utils.read_puzzle_input("inputs/day17.txt")
    registers, instructions = utils.split_list_at(puzzle_input, pat="")

    registers = [utils.nums(line)[0] for line in registers]
    instructions = utils.nums(instructions[0])

    def extend_register(register_value: int, to_generate: list[int]) -> list[int]:
        """Recursively add to the seed so we start generating the tail of the output.

        The main insight is that:
        - A needs to end up being 0 at the end to terminate the program.
        - In step n-1 before the end, only the lowest 3 bits of A determine output
        - After that, the lowest 3 bits get shifted up in each iteration and we just
          need to test how to set the next 3 bits, which are now the lowest.
        - Important: For 3 given bits, there might be multiple patterns that yield
          a given output, so we need to try all of them and not take the first best,
          which may lead us into a dead end later.

        See the day17.svg for the visualization I've used to understand this pattern.
        """

        if len(to_generate) == 0:
            return [register_value]

        candidates = []
        for i in range(8):
            registers[0] = (register_value << 3) | i

            program = ProgramState(registers)
            program.run_instructions(instructions)

            if program.outputs[0] == to_generate[-1]:
                candidates.extend(
                    extend_register(
                        register_value=(register_value << 3) | i,
                        to_generate=to_generate[:-1],
                    )
                )

        return candidates

    register_candidates = extend_register(register_value=0, to_generate=instructions)

    # The first candidate is the smallest, since sort of recursed in-order, with smaller bits first.
    registers[0] = register_candidates[0]
    program = ProgramState(registers)
    program.run_instructions(instructions)
    print(program.outputs)


if __name__ == "__main__":
    main()
