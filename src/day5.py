import utils


def main():
    puzzle_input = utils.read_puzzle_input("inputs/example5.txt")
    puzzle_input = utils.read_puzzle_input("inputs/day5.txt")

    rules, pages = utils.split_list_at(puzzle_input, pat="")

    nodes = {node for rule in rules for node in utils.nums(rule)}
    rule_map = {n: set() for n in nodes}

    for rule in rules:
        a, b = rule.split("|")
        rule_map[int(a)].add(int(b))

    correct_middle_numbers = []
    incorrect_middle_numbers = []

    for update in (utils.nums(p) for p in pages):
        if check_order(update, rule_map):
            correct_middle_numbers.append(update[len(update) // 2])
        else:
            update_set = set(update)
            sub_graph = {k: (v & update_set) for k, v in rule_map.items() if k in update_set}
            topo_sort = toplogical_sort(sub_graph)
            incorrect_middle_numbers.append(topo_sort[len(topo_sort) // 2])

    print(f"Correct updates:   {sum(correct_middle_numbers)}")
    print(f"Incorrect updates: {sum(incorrect_middle_numbers)}")


def toplogical_sort(graph: dict[int, set[int]]) -> list[int]:
    """Topological sort by iteratively removing the in-degree 0 node.

    Runtime seems to be slower than possible if I maintained a set of 0-in-degree nodes instead.
    """
    topo_sort = []

    in_degrees = get_graph_in_degrees(graph)
    while len(graph) > 0:
        # Would be faster to maintain a set of these instead of searching anew each time.
        min_node, min_count = min(in_degrees.items(), key=lambda kv: kv[1])
        assert min_count == 0, "Graph has a cycle"

        # Adjust in-degree of neighbors of now deleted node.
        for neighbor in graph[min_node]:
            in_degrees[neighbor] -= 1

        # Actually delete the node.
        del graph[min_node]
        del in_degrees[min_node]

        topo_sort.append(min_node)

    return topo_sort


def get_graph_in_degrees(graph: dict[int, set[int]]) -> dict[int, int]:
    # Bit weird, but our adjacency list doesn't contain in degree 0 nodes otherwise.
    nodes = set(graph.keys()) | set().union(*[v for v in graph.values()])

    in_degrees = {n: 0 for n in nodes}
    for targets in graph.values():
        for t in targets:
            in_degrees[t] += 1

    return in_degrees


def check_order(update: list[int], rule_map: dict[int, set[int]]) -> bool:
    for i in range(len(update)):
        num = update[i]
        following_nums = set(update[i + 1 :])

        if not following_nums <= rule_map[num]:
            return False

    return True


if __name__ == "__main__":
    main()
