import utils


def main():
    puzzle_input = utils.read_example_input("""2333133121414131402""")[0]
    puzzle_input = utils.read_puzzle_input("inputs/day9.txt")[0]

    part1(puzzle_input)
    part2(puzzle_input)


def part1(puzzle_input: str):
    """Part 1 I just did by swapping out individual positions."""
    id_counter = 0

    disk_layout = []

    empty_index = []
    non_empty_index = []

    id_counter = 0
    for i, c in enumerate(puzzle_input):
        if i % 2 == 0:
            next_val = id_counter
            id_counter += 1
        else:
            next_val = EMPTY

        for _ in range(int(c)):
            disk_layout.append(next_val)

            list_pos = len(disk_layout) - 1
            if next_val == EMPTY:
                empty_index.insert(0, list_pos)
            else:
                non_empty_index.append(list_pos)

    for _ in range(len(disk_layout)):
        first_empty = empty_index.pop()
        first_non_empty = non_empty_index.pop()

        disk_layout[first_empty] = disk_layout[first_non_empty]
        disk_layout[first_non_empty] = EMPTY

        if empty_index[-1] > non_empty_index[-1]:
            break

    checksum = sum([(i * v) if v != EMPTY else 0 for i, v in enumerate(disk_layout)])
    print(checksum)


EMPTY = -1


def part2(puzzle_input: str):
    """For part 2, we had to consider whole blocks."""
    empty_blocks = []  # Store (position, length)
    file_blocks = []  # Store (position, length, file-ID)

    pos_counter = 0
    for i, c in enumerate(puzzle_input):
        block_len = int(c)
        if i % 2 == 0:
            file_blocks.append((pos_counter, block_len, len(file_blocks)))
        else:
            empty_blocks.append((pos_counter, block_len))

        pos_counter += block_len

    final_files = []
    # Attempt to move each file exactly once.
    for file_pos, file_len, file_id in reversed(file_blocks):
        remaining_empty_blocks = []

        # Find the next free empty block to the left of the file block position.
        for i, (empty_pos, empty_len) in enumerate(empty_blocks):
            if (empty_pos < file_pos) and (empty_len >= file_len):
                final_files.append((empty_pos, file_len, file_id))

                # Put the rest of the free space back into the block pool, plus all following ones.
                remaining_empty_blocks.append((empty_pos + file_len, empty_len - file_len))
                remaining_empty_blocks.extend(empty_blocks[i + 1 :])
                break
            else:
                remaining_empty_blocks.append((empty_pos, empty_len))
        else:
            # If we didn't find a place for this file, it will remain where it is.
            final_files.append((file_pos, file_len, file_id))

        empty_blocks = remaining_empty_blocks

    checksum = sum(
        [
            (file_id * pos)
            for (file_pos, file_len, file_id) in final_files
            for pos in range(file_pos, file_pos + file_len)
        ]
    )
    print(checksum)


if __name__ == "__main__":
    main()
