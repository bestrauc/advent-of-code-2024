import utils
from collections import defaultdict

NUMBER_KEYPAD = [
    ["7", "8", "9"],
    ["4", "5", "6"],
    ["1", "2", "3"],
    [" ", "0", "A"],
]

ARROW_KEYPAD = [
    [" ", "^", "A"],
    ["<", "v", ">"],
]


def main():
    puzzle_input = utils.read_example_input(
        """029A
980A
179A
456A
379A"""
    )
    puzzle_input = utils.read_puzzle_input("inputs/day21.txt")

    score_sum = 0
    for sequence in puzzle_input:
        min_numpad = float("inf")
        min_keypad1 = float("inf")
        min_keypad2 = float("inf")

        min_score = float("inf")
        min_seq = None

        code_value = utils.nums(sequence)[0]
        possible_numpad_moves = get_move_sequence(NUMBER_KEYPAD, input_sequence=sequence)
        for numpad_moves in possible_numpad_moves:
            moves_on_keypad(NUMBER_KEYPAD, numpad_moves)
            if len(numpad_moves) > min_numpad:
                continue
            min_numpad = min(min_numpad, len(numpad_moves))

            possible_keypad1_moves = get_move_sequence(ARROW_KEYPAD, input_sequence=numpad_moves)
            for keypad1_moves in possible_keypad1_moves:
                if len(keypad1_moves) > min_keypad1:
                    continue
                min_keypad1 = min(min_keypad1, len(keypad1_moves))

                possible_keypad2_moves = get_move_sequence(ARROW_KEYPAD, input_sequence=keypad1_moves)
                for keypad2_moves in possible_keypad2_moves:
                    print("".join(keypad2_moves))
                    if len(keypad2_moves) > min_keypad2:
                        continue
                    min_keypad2 = min(min_keypad2, len(keypad2_moves))

                    score = len(keypad2_moves) * code_value
                    if min_score > score:
                        min_score = score
                        min_seq = keypad2_moves

        print(f"{sequence}: {''.join(min_seq)} (len={len(min_seq)}, score={min_score})")
        score_sum += min_score

    print(score_sum)


def moves_on_keypad(keypad: list[list[str]], moves: list[str]) -> list[str]:
    h, w = utils.input_dim(keypad)
    button_pos = {keypad[i][j]: (i, j) for i in range(h) for j in range(w)}

    buttons_input = []
    bi, bj = button_pos["A"]
    for c in moves:
        if c == "A":
            buttons_input.append(keypad[bi][bj])
            continue

        (di, dj) = utils.MOVE_TO_DX[c]
        bi, bj = bi + di, bj + dj
        assert keypad[bi][bj] != " "

    return buttons_input


def get_move_sequence(keypad: list[list[str]], input_sequence: list[str]) -> list[str]:
    h, w = utils.input_dim(keypad)
    button_pos = {keypad[i][j]: (i, j) for i in range(h) for j in range(w)}

    total_moves = [[]]

    last_button = "A"
    for next_button in input_sequence:
        _, previous = shortest_path(start=button_pos[last_button], grid=keypad)
        moves = get_moves_rec(previous, target=button_pos[next_button])
        moves = [m + ["A"] for m in moves]

        total_moves = [t + m for t in total_moves for m in moves]

        last_button = next_button

    return total_moves


def get_moves(previous: dict, target: tuple[int, int]) -> list[str]:
    moves = []

    node = target
    while previous[node] is not None:
        (i, j) = node
        (pi, pj) = previous[node]
        moves.append(utils.DX_TO_MOVE[(i - pi, j - pj)])

        node = previous[node]

    return list(reversed(moves))


def get_moves_rec(previous: dict, target: tuple[int, int]) -> list[str]:
    if len(previous[target]) == 0:
        return [[]]

    all_moves = []

    (ti, tj) = target
    for prev in previous[target]:
        (pi, pj) = prev
        move_char = utils.DX_TO_MOVE[(ti - pi, tj - pj)]
        for prev_move in get_moves_rec(previous, target=prev):
            all_moves.append(prev_move + [move_char])

    return all_moves


def shortest_path(start: tuple[int, int], grid: list[list[str]], level: int = 0) -> tuple[dict, dict]:
    h, w = utils.input_dim(grid)

    q = utils.PriorityQueue()

    distances = defaultdict(lambda: 100000000000)
    distances[start] = 0

    previous = {start: set()}

    q.add_task(start)

    while len(q.pq) > 0:
        node = q.pop_task()
        (i, j) = node

        adj_neighbors = [
            (i + di, j + dj)
            for (di, dj) in utils.ADJ4
            # A valid neighbor is on the keypad and isn't the empty button, which we shouldn't use.
            if (i + di) in range(h) and (j + dj) in range(w) and grid[i + di][j + dj] != " "
        ]
        neighbors = [(ni, nj) for (ni, nj) in adj_neighbors]

        for neighbor in neighbors:
            if distances[neighbor] > distances[node] + 1:
                previous[neighbor] = {node}
                distances[neighbor] = distances[node] + 1
                q.add_task(neighbor)
            elif distances[neighbor] == distances[node] + 1:
                previous[neighbor] |= {node}

    return distances, previous


if __name__ == "__main__":
    main()
