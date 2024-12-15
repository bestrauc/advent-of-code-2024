import utils

MOVE_MAP = {
    "^": (-1, 0),
    "v": (1, 0),
    "<": (0, -1),
    ">": (0, 1),
}


def main():
    puzzle_input = utils.read_puzzle_input("inputs/day15_large_example.txt")
    # puzzle_input = utils.read_puzzle_input("inputs/day15.txt")
    grid, moves = utils.split_list_at(puzzle_input, pat="")
    grid = [list(line) for line in grid]
    moves = [c for line in moves for c in line]

    wide_grid = expand_map(grid)
    utils.print_grid(wide_grid)

    for move in moves:
        print(f"Move {move}:")
        move_robot(wide_grid, move)
        utils.print_grid(wide_grid)
        print()

    utils.print_grid(wide_grid)
    print(box_coordinate_sum(wide_grid))


def move_robot(grid: list[list[str]], direction: str):
    h, w = utils.input_dim(grid)

    di, dj = MOVE_MAP[direction]
    ri, rj = [(i, j) for i in range(h) for j in range(w) if grid[i][j] == "@"][0]
    ni, nj = (ri + di, rj + dj)

    # We'd be moving against a wall -> don't move.
    if grid[ni][nj] == "#":
        return

    def move_boxes(bi: int, bj: int, check_only: bool) -> bool:
        """Move the stack of boxes at this position out of the way.

        Can also check first if a move is possible, because when we choose
        to move, we do it "depth-first" and start moving boxes around already.
        So we have to make sure first that all moves are possible at the end.

        This function is recursive and moves the boxes when unwinding. Probably
        a bit too complicated and verbose with the cases, but it works! :D
        """
        if grid[bi][bj] not in "[]":
            return True

        # This is the coordinate of the other half of the box
        b2i, b2j = (bi, bj + 1) if grid[bi][bj] == "[" else (bi, bj - 1)

        # We'd move the box to these locations.
        b_ni, b_nj = (bi + di), (bj + dj)
        b2_ni, b2_nj = (b2i + di), (b2j + dj)

        # Horizontal moves are easy, no overlapping box complications.
        if di == 0:
            if grid[b_ni][b_nj] == "#":
                return False
            elif grid[b_ni][b_nj] == ".":
                if not check_only:
                    grid[b_ni][b_nj] = grid[bi][bj]
                    grid[bi][bj] = "."

                return True
            elif grid[b_ni][b_nj] in "[]":
                move_possible = move_boxes(b_ni, b_nj, check_only)
                if move_possible and not check_only:
                    grid[b_ni][b_nj] = grid[bi][bj]
                    grid[bi][bj] = "."

                return move_possible
        # Vertical moves have to account for overlapping boxes.
        else:
            # One of the two halves can't be moved.
            if (grid[b_ni][b_nj] == "#") or (grid[b2_ni][b2_nj] == "#"):
                return False
            # Both halves can be moved.
            elif (grid[b_ni][b_nj] == ".") and (grid[b2_ni][b2_nj] == "."):
                if not check_only:
                    grid[b_ni][b_nj] = grid[bi][bj]
                    grid[bi][bj] = "."

                    grid[b2_ni][b2_nj] = grid[b2i][b2j]
                    grid[b2i][b2j] = "."

                return True
            # At least one of the two halves would push another box.
            elif (grid[b_ni][b_nj] in "[]") or (grid[b2_ni][b2_nj] in "[]"):
                move_possible1 = move_boxes(b_ni, b_nj, check_only)
                move_possible2 = move_boxes(b2_ni, b2_nj, check_only)

                if move_possible1 and move_possible2 and not check_only:
                    grid[b_ni][b_nj] = grid[bi][bj]
                    grid[bi][bj] = "."

                    grid[b2_ni][b2_nj] = grid[b2i][b2j]
                    grid[b2i][b2j] = "."

                return move_possible1 and move_possible2

    if move_boxes(ni, nj, check_only=True):
        move_boxes(ni, nj, check_only=False)

    # Move the robot if possible
    if grid[ni][nj] == ".":
        grid[ni][nj] = "@"
        grid[ri][rj] = "."


def box_coordinate_sum(grid: list[list[str]]) -> int:
    h, w = utils.input_dim(grid)
    box_positions = [(i, j) for i in range(h) for j in range(w) if grid[i][j] in "[O"]
    return sum(100 * i + j for (i, j) in box_positions)


def expand_map(grid: list[list[str]]) -> list[list[str]]:
    new_grid = []
    h, w = utils.input_dim(grid)
    for i in range(h):
        line = []
        for j in range(w):
            if grid[i][j] == "O":
                line.append("[")
                line.append("]")
            elif grid[i][j] == "@":
                line.append("@")
                line.append(".")
            else:
                line.append(grid[i][j])
                line.append(grid[i][j])

        new_grid.append(line)

    return new_grid


if __name__ == "__main__":
    main()
