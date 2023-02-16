# _resources.py
from __future__ import annotations

from collections import defaultdict
from textwrap import TextWrapper
from typing import NamedTuple

"""Resources for solutions to David Amos's weekly coding challenge for 2023-02-13:
    https://discourse.davidamos.dev/t/flight-inference/135
"""


class DirectedGraph(NamedTuple):
    vertices: list[str]
    edges: dict[str, list[str]]

    @classmethod
    def read_file(cls: type[DirectedGraph], filename: str) -> DirectedGraph:
        """Read a directed graph dataset."""
        with open(filename, "rt") as infile:
            data = infile.read()
        return cls.read_string(data)

    @classmethod
    def read_string(cls: type[DirectedGraph], data: str) -> DirectedGraph:
        """Read a directed graph dataset from str."""
        edges = [
            ((k := line.split())[0].strip(), k[1].strip()) for line in data.splitlines()
        ]
        edge_dict: defaultdict[str, list[str]] = defaultdict(list)
        vertices: set[str] = set()
        for e0, e1 in edges:
            edge_dict[e0].append(e1)
            vertices.add(e0)
            vertices.add(e1)
        return DirectedGraph(list(vertices), edge_dict)


def format_answer(output: dict[str, list[str]]) -> str:
    """Produce a nicely formatted answer."""
    wrapper = TextWrapper(width=75, subsequent_indent=" " * 4)
    out_str = ""
    for key, val in sorted(output.items()):
        out_str += wrapper.fill(f"{key}: " + ", ".join(sorted(val))) + "\n"
    return out_str
