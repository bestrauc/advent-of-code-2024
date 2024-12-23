"""This is a bit of a mess, but eventually I did it.

The gist of it is that I iterate overall possible input patterns for a given
abstraction level, for instance for the first level:

382A can be input via these strokes, separated per character:
    ['^', 'A'], ['^', '^', '<', 'A'], ['v', 'v', 'A'], ['v', '>', 'A']
    ['^', 'A'], ['^', '^', '<', 'A'], ['v', 'v', 'A'], ['>', 'v', 'A']
    ['^', 'A'], ['<', '^', '^', 'A'], ['v', 'v', 'A'], ['v', '>', 'A']
    ['^', 'A'], ['<', '^', '^', 'A'], ['v', 'v', 'A'], ['>', 'v', 'A']

I do not just find one shortest path, but all equivalent shortest ones, 
which makes reconstructing the paths a bit of a mess. However, this could
easily be precomputed once for both keypads.

Note that I use Dijkstra to find these patterns, which is possibly overkill,
but there I could easily exclude patterns like ^>^>, which would just cause
unnecessary turns, which cause excessive inputs on higher level keypads.

I don't think this optimization is really necessary once you get the iteration
order and the caching right, but I did it while I was exploring things.

So I have a generator for these inputs and iterate over them like thus:

- ['^', 'A']
    - ['^', '^', '<', 'A']
        - ['v', 'v', 'A']
            - ['v', '>', 'A']
            - ['>', 'v', 'A']
    - ['<', '^', '^', 'A']
        - ['v', 'v', 'A']
            - ['v', '>', 'A']
            - ['>', 'v', 'A']

And for each level, I recurse into the keypads to find the shortest input
sequence for them. So runtime-wise, we definitely have to walk this graph
once, but note for example that we can cache the lower levels: The pattern
['v', '>', 'A'] occurs twice at the bottom, so we only have to compute its
shortest keypad-length once and the same for higher-up nodes, etc.

Initially I tried to generate the actual shortest sequence and measure its
lenght, but that was way too slow and not cacheable - the solution is a
few billion characters long, after all and we have to cache a few options.
In the end, just caching the lengths of the subproblems was enough, however.
"""

import utils
from collections import defaultdict
import functools

NUMBER_KEYPAD = (
    ("7", "8", "9"),
    ("4", "5", "6"),
    ("1", "2", "3"),
    (" ", "0", "A"),
)

ARROW_KEYPAD = (
    (" ", "^", "A"),
    ("<", "v", ">"),
)


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
        code_value = utils.nums(sequence)[0]
        min_move_len = min_moves(keypad=NUMBER_KEYPAD, sequence=tuple(sequence), depth=26)

        score = min_move_len * code_value
        score_sum += score

    print(score_sum)


@functools.cache
def min_moves(keypad: tuple[tuple[str]], sequence: tuple[str], depth: int = 0) -> int:
    if depth == 0:
        return len(sequence)

    possible_moves_tree = get_move_tree(keypad=keypad, sequence=sequence)

    min_seq_len = None
    for possible_moves in possible_moves_tree:
        ongoing_seq_len = 0
        for move in possible_moves:
            min_move_len = min_moves(keypad=ARROW_KEYPAD, sequence=tuple(move), depth=depth - 1)
            ongoing_seq_len += min_move_len

        if min_seq_len is None or ongoing_seq_len < min_seq_len:
            min_seq_len = ongoing_seq_len

    return min_seq_len


def get_move_tree(keypad: tuple[tuple[str]], sequence: tuple[str], last_button: str = "A"):
    """Recursive way of generating all the ways you can input the sequence."""
    if len(sequence) == 0:
        yield []
        return

    h, w = utils.input_dim(keypad)
    button_pos = {keypad[i][j]: (i, j) for i in range(h) for j in range(w)}

    next_button = sequence[0]
    dists1, previous1 = shortest_path(start=(*button_pos[last_button], "|"), grid=keypad)
    dists2, previous2 = shortest_path(start=(*button_pos[last_button], "-"), grid=keypad)

    # Because my shortest path algorithm punishes turns, we have to find the possible
    # shortest paths by checking out all the horizontal/vertical starts and endings.
    min_dist = min(
        dists1[(*button_pos[next_button], "|")],
        dists1[(*button_pos[next_button], "-")],
        dists2[(*button_pos[next_button], "|")],
        dists2[(*button_pos[next_button], "-")],
    )

    moves = []
    if min_dist == dists1[(*button_pos[next_button], "|")]:
        moves += get_moves_rec(previous1, target=(*button_pos[next_button], "|"))
    if min_dist == dists1[(*button_pos[next_button], "-")]:
        moves += get_moves_rec(previous1, target=(*button_pos[next_button], "-"))
    if min_dist == dists2[(*button_pos[next_button], "|")]:
        moves += get_moves_rec(previous2, target=(*button_pos[next_button], "|"))
    if min_dist == dists2[(*button_pos[next_button], "-")]:
        moves += get_moves_rec(previous2, target=(*button_pos[next_button], "-"))

    # Combine the various ways we can get this char with the ways we can generate the remaining ones.
    moves = [m + ["A"] for m in moves]
    yield from ([m] + t for m in moves for t in get_move_tree(keypad, last_button=next_button, sequence=sequence[1:]))


def get_moves_rec(previous: dict, target: tuple[int, int]) -> list[str]:
    if len(previous[target]) == 0:
        return [[]]

    all_moves = []

    (ti, tj, t_axis) = target
    for prev in previous[target]:
        (pi, pj, p_axis) = prev

        # Don't add a movement for rotations.
        if (ti == pi) and (tj == pj):
            for prev_move in get_moves_rec(previous, target=prev):
                all_moves.append(prev_move)
        else:
            move_char = utils.DX_TO_MOVE[(ti - pi, tj - pj)]
            for prev_move in get_moves_rec(previous, target=prev):
                all_moves.append(prev_move + [move_char])

    return all_moves


AXIS_NEIGHBORS = {
    "|": [(-1, 0), (1, 0)],
    "-": [(0, -1), (0, 1)],
}


def shortest_path(start: tuple[int, int], grid: list[list[str]]) -> tuple[dict, dict]:
    h, w = utils.input_dim(grid)

    q = utils.PriorityQueue()

    distances = defaultdict(lambda: 100000000000)
    distances[start] = 0

    previous = {start: set()}

    q.add_task(start)

    while len(q.pq) > 0:
        node = q.pop_task()
        (i, j, axis) = node

        # We can continue in either direction on our axis.
        neighbors = [((i + di, j + dj, axis), 1) for (di, dj) in AXIS_NEIGHBORS[axis]]

        # Or we rotate, at a high cost.
        neighbors += [((i, j, "|" if axis == "-" else "-"), 1000)]

        neighbors = [
            ((ni, nj, axis), cost)
            for ((ni, nj, axis), cost) in neighbors
            # A valid neighbor is on the keypad and isn't the empty button, which we shouldn't use.
            if ni in range(h) and nj in range(w) and grid[ni][nj] != " "
        ]

        for neighbor, cost in neighbors:
            if distances[neighbor] > distances[node] + cost:
                previous[neighbor] = {node}
                distances[neighbor] = distances[node] + cost
                q.add_task(neighbor)
            elif distances[neighbor] == distances[node] + cost:
                previous[neighbor] |= {node}

    return distances, previous


if __name__ == "__main__":
    main()
