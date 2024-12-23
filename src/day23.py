import utils
from collections import defaultdict
import itertools

import networkx as nx


def main():
    puzzle_input = utils.read_example_input(
        """kh-tc
qp-kh
de-cg
ka-co
yn-aq
qp-ub
cg-tb
vc-aq
tb-ka
wh-tc
yn-cg
kh-ub
ta-co
de-co
tc-td
tb-wq
wh-td
ta-ka
td-qp
aq-cg
wq-ub
ub-vc
de-ta
wq-aq
wq-vc
wh-yn
ka-de
kh-ta
co-tc
wh-qp
tb-vc
td-yn"""
    )
    puzzle_input = utils.read_puzzle_input("inputs/day23.txt")

    graph_map = defaultdict(list)
    for line in puzzle_input:
        node1, node2 = line.split("-")
        graph_map[node1].append(node2)
    graph = nx.Graph(graph_map)

    k = 3
    k_cliques_with_t = set()
    max_clique = ()
    for clique in nx.find_cliques(graph):
        if len(clique) < k:
            continue

        # Sorting is necessary for consistent subclique-enumeration below
        # and to output the max clique nodes in the order required by AoC.
        clique = tuple(sorted(clique))

        # Keep track of this for part 2.
        if len(clique) > len(max_clique):
            max_clique = clique

        # `nx.find_cliques` finds maximal cliques of size n, but for the ones with n > k,
        # we can just iterate through all the (n choose k) sub-cliques with these nodes.
        for k_clique in itertools.combinations(clique, k):
            if any(node.startswith("t") for node in k_clique):
                # Cliques can overlap, e.g. [A,B,C,D] and [B,C,D,E] can be maximal cliques
                # for nodes A and E, respectively, but the subset [B,C,D] will occur in both.
                # So we have to collect them into a set to deduplicate them.
                k_cliques_with_t.add(k_clique)

    print(f"3-cliques with t: {len(k_cliques_with_t)}")
    print(f"Password: {','.join(max_clique)}")


if __name__ == "__main__":
    main()
