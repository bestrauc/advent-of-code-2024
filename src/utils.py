import re
import itertools
import heapq

ADJ4 = [(-1, 0), (1, 0), (0, -1), (0, 1)]


def split_list_at(l: list, pat: str) -> list[list]:
    try:
        idx = l.index(pat)
    except ValueError:
        return [l]

    return [l[:idx]] + split_list_at(l[idx + 1 :], pat)


def read_puzzle_input(input_path: str) -> list[str]:
    return [l.strip() for l in open(input_path).readlines()]


def read_example_input(input_str: str) -> list[str]:
    return [l.strip() for l in input_str.split("\n")]


def nums(line: str) -> list[int]:
    return [int(n) for n in re.findall(r"(-*\d+)", line)]


def input_dim(inp: list[str]) -> tuple[int, int]:
    """Return (height, width) of a 2D input."""
    return len(inp), len(inp[0])


def transpose(l: list[list]) -> list[list]:
    return list(map(list, zip(*l)))


def print_grid(grid: list[list[str]]):
    print("\n".join("".join(row) for row in grid))


class PriorityQueue:
    """A wrapper around the queue implementation suggested by the heapq docs."""

    def __init__(self):
        self.pq = []  # list of entries arranged in a heap
        self.entry_finder = {}  # mapping of tasks to entries
        self.REMOVED = "<removed-task>"  # placeholder for a removed task
        self.counter = itertools.count()  # unique sequence count

    def add_task(self, task, priority=0):
        "Add a new task or update the priority of an existing task"
        if task in self.entry_finder:
            self.remove_task(task)
        count = next(self.counter)
        entry = [priority, count, task]
        self.entry_finder[task] = entry
        heapq.heappush(self.pq, entry)

    def remove_task(self, task):
        "Mark an existing task as REMOVED.  Raise KeyError if not found."
        entry = self.entry_finder.pop(task)
        entry[-1] = self.REMOVED

    def pop_task(self):
        "Remove and return the lowest priority task. Raise KeyError if empty."
        while self.pq:
            priority, count, task = heapq.heappop(self.pq)
            if task is not self.REMOVED:
                del self.entry_finder[task]
                return task

        raise KeyError("pop from an empty priority queue")
