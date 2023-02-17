# make_random_examples.py
from __future__ import annotations

import random
from collections.abc import Sequence
from dataclasses import dataclass
from math import fsum

from _resources import DirectedGraph


@dataclass(frozen=True)
class Node:
    location: tuple[float, float, float, float]
    importance: float
    perturbation: float

    @classmethod
    def squared_dist(cls: type[Node], a: Node, b: Node) -> float:
        return (
            fsum((x - y) ** 2 for x, y in zip(a.location, b.location))
            + a.perturbation * b.perturbation
        )

    @classmethod
    def attraction(cls: type[Node], a: Node, b: Node) -> float:
        return a.importance * b.importance / cls.squared_dist(a, b)

    @classmethod
    def random_node(cls: type[Node]) -> Node:
        return cls(
            tuple([random.normalvariate() for _ in range(4)]),
            random.normalvariate(),
            random.normalvariate() / 1_000,
        )

    @classmethod
    def random_graph(cls: type[Node], num_nodes: int, num_edges: int) -> DirectedGraph:
        node_dict = {k: cls.random_node() for k in range(num_nodes)}
        id_len = len(str(num_nodes))
        node_fmt = "v{" + f":0{id_len}d" + "}"
        node_list = [node_fmt.format(k) for k in range(num_nodes)]
        attractions = sorted(
            [
                (cls.attraction(node_dict[j], node_dict[k]), j, k)
                for j in range(num_nodes)
                for k in range(j)
            ]
        )
        target_sum = fsum(a[0] for a in attractions) / num_edges
        edge_pools: list[list[tuple[int, int]]] = [[]] * num_edges
        pool_sums = [0] * num_edges
        for idx, a in enumerate(attractions):
            for p in range(num_edges):
                if ((ps := pool_sums[p]) == 0 or ps + a[0] < target_sum) and (
                    len(attractions) - idx <= num_edges - p
                ):
                    edge_pools[p].append((a[1], a[2]))
                    break

        edges_raw = [
            (node_list[(e := random.choice(p))[0]], node_list[e[1]]) for p in edge_pools
        ]
        edges = [random.choice([(p[1], p[0]), p]) for p in edges_raw]
        edge_dict = {k: [e[1] for e in edges if e[0] == k] for k in node_list}
        return DirectedGraph(node_list, edge_dict)


if __name__ == "__main__":
    for k in range(4):
        g = Node.random_graph(25, 20)
        with open(f"random_{k}.txt", "wt") as outfile:
            outfile.write(g.output_graph())
