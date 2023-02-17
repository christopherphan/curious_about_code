# make_super_example.py

"""Make a very large digraph."""

from collections import defaultdict
from collections.abc import Iterator, Sequence
from typing import Final

from _resources import DirectedGraph

TEMPLATES: Final[list[str]] = [
    "\n".join(f"{j} {u}" for (j, k) in g for u in k)
    for g in [
        [("A", "BC"), ("B", "DY"), ("C", "E"), ("D", "Z"), ("E", "Z")],
        [
            ("A", "GH"),
            ("B", "CD"),
            ("C", "E"),
            ("D", "EF"),
            ("G", "IY"),
            ("H", "Y"),
            ("I", "KL"),
            ("F", "KL"),
            ("K", "Z"),
            ("L", "Z"),
        ],
        [("A", "BC"), ("B", "G"), ("C", "D"), ("D", "BE"), ("E", "YZ")],
        [("A", "BC"), ("B", "Z"), ("C", "DY"), ("D", "E"), ("E", "F"), ("F", "C")],
    ]
]

GRAPHS: Final[list[DirectedGraph]] = [DirectedGraph.read_string(k) for k in TEMPLATES]


def graph_cycler(graphs: Sequence[DirectedGraph]) -> Iterator[DirectedGraph]:
    num_graphs = len(graphs)
    k = 0
    while True:
        yield graphs[k % num_graphs]
        k += 1


def complicate(graph: DirectedGraph, cycler: Iterator[DirectedGraph]) -> DirectedGraph:
    new_edges: dict[str, list[str]] = defaultdict(list)
    new_vertices: set[str] = set()
    for vert, edge_list in graph.edges.items():
        subgraph = next(cycler)
        new_vertices |= set(f"{vert}_{sub_vert}" for sub_vert in subgraph.vertices)
        for sub_vert, sub_edges in subgraph.edges.items():
            new_edges[f"{vert}_{sub_vert}"].extend(
                [f"{vert}_{dest}" for dest in sub_edges]
            )
        s_sub_verts = sorted(subgraph.vertices)
        for idx, dest in enumerate(edge_list):
            new_edges[f"{vert}_{s_sub_verts[-idx - 1]}"].append(f"{dest}_A")
    return DirectedGraph(list(new_vertices), new_edges)


def main():
    cycler = graph_cycler(GRAPHS)
    graph = next(cycler)
    for _ in range(3):
        graph = complicate(graph, cycler)
    print(graph.output_graph)


if __name__ == "__main__":
    main()
