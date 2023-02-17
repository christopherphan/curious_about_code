# test.py

from collections.abc import Callable
from typing import Final

import graphdestinations
import matrix
import matrix2
from _resources import DirectedGraph, format_answer

GRAPHS: Final[list[DirectedGraph]] = [
    DirectedGraph.read_file(k)
    for k in ["example.txt", "flights1.txt", "gistfile1.txt"]
    + [f"random_{z}.txt" for z in range(4)]
]

EXAMPLE_SOLN: Final[
    str
] = """A: B, D, E
B: A, D, E
C: A, B, D, E
D:
E: A, B, D"""


def test_graphdestinations():
    graph = DirectedGraph.read_file("example.txt")
    assert format_answer(graphdestinations.reachable(graph)).strip() == EXAMPLE_SOLN


def test_functions():
    funcs = [matrix.reachable, matrix2.reachable]
    for g in GRAPHS:
        for f in funcs:
            assert process_soln(f(g)) == process_soln(graphdestinations.reachable(g))


def process_soln(soln: dict[str, list[str]]) -> frozenset[tuple[str, frozenset[str]]]:
    """Change solution so that the order of elements listed is irrelvent."""
    return frozenset([(key, frozenset(value)) for key, value in soln.items()])
