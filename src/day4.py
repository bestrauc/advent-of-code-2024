import utils
import numpy as np

puzzle_input = utils.read_example_input(
    """MMMSXXMASM
MSAMXMSMSA
AMXSXMAAMM
MSAMASMSMX
XMASAMXAMM
XXAMMXXAMA
SMSMSASXSS
SAXAMASAAA
MAMMMXMMMM
MXMXAXMASX"""
)
puzzle_input = utils.read_puzzle_input("inputs/day4.txt")
puzzle_input = list(map(list, puzzle_input))

text_array = np.array(puzzle_input)


def search_rows(text_array: np.ndarray, pattern: np.ndarray) -> int:
    return sum(np.apply_along_axis(search_array, 1, text_array, pattern))


def search_diagonals(text: np.ndarray, pattern: str) -> int:
    h, w = text.shape
    matches = 0
    for offset in range(-h + 1, w):
        diag = np.diagonal(text, offset=offset)
        matches += search_array(diag, pattern)

    return matches


def search_array(text: np.ndarray, pattern: np.ndarray) -> int:
    if len(text) < len(pattern):
        return 0

    rev_pattern = pattern[::-1]
    view = np.lib.stride_tricks.sliding_window_view(text, len(pattern))
    return (view == pattern).all(axis=1).sum() + (view == rev_pattern).all(axis=1).sum()


pattern = np.array(list("XMAS"))

row_hits = search_rows(text_array, pattern)
col_hits = search_rows(text_array.T, pattern)
diag_hits = search_diagonals(text_array, pattern)
inv_diag_hits = search_diagonals(np.fliplr(text_array), pattern)
total = row_hits + col_hits + diag_hits + inv_diag_hits

print(f"Row {row_hits}, Col {col_hits}, Diag {diag_hits + inv_diag_hits}: Total {total}")

# Part 2
views = np.lib.stride_tricks.sliding_window_view(text_array, (3, 3))

x_pattern = np.array(list("MAS"))
x_mas_matches = 0
for window in views.reshape(-1, 3, 3):
    diag1 = window.diagonal()
    diag1_match = (diag1 == x_pattern).all() or (diag1[::-1] == x_pattern).all()

    diag2 = np.fliplr(window).diagonal()
    diag2_match = (diag2 == x_pattern).all() or (diag2[::-1] == x_pattern).all()

    if diag1_match and diag2_match:
        x_mas_matches += 1

print(x_mas_matches)
