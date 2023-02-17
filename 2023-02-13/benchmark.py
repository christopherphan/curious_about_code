# benchmark.py

"""Perform benchmarks for David Amos's weekly coding challenge for 2023-02-13:
    https://discourse.davidamos.dev/t/flight-inference/135
"""

import timeit
from typing import Final, NamedTuple

import rich.box
from rich.console import Console
from rich.table import Table

from _resources import DirectedGraph


class TimeTest(NamedTuple):
    """Represent a file and module combo to test with timeit."""

    import_str: str
    graph_file: str


def make_timer(tt: TimeTest) -> timeit.Timer:
    """Produce a Timer object for the given time test."""
    return timeit.Timer(
        "reachable(graph)",
        setup=tt.import_str
        + "\nfrom _resources import DirectedGraph"
        + f"\n\ngraph = DirectedGraph.read_file({tt.graph_file!r})",
    )


def run_time_test(tt: TimeTest, num_repeat: int) -> float:
    """Run the time test and give the return time per execusion."""
    t = make_timer(tt)
    return max(k / num_repeat for k in t.repeat(number=num_repeat))


if __name__ == "__main__":
    IMPORTS: Final[list[str]] = [
        "graphdestinations",
        "optimizedgraphdest",
        "matrix",
        "matrix2",
    ]
    GRAPH_FILES: Final[dict[str, tuple[int, list[str]]]] = {
        "flights1.txt": (10_000, []),
        "gistfile1.txt": (1_000, []),
        "super_example.txt": (3, ["matrix", "matrix2"]),
    } | {f"random_{k}.txt": (500, []) for k in range(4)}
    console = Console()

    graphtable = Table(title="Graphs", box=rich.box.MARKDOWN)
    graphtable.add_column("File")
    graphtable.add_column("# vertices", justify="right")
    graphtable.add_column("# edges", justify="right")
    graphtable.add_column("Execusions per trial", justify="right")
    for v, k in GRAPH_FILES.items():
        g = DirectedGraph.read_file(v)
        graphtable.add_row(
            v,
            "{:,}".format(len(g.vertices)),
            "{:,}".format(sum(len(e) for e in g.edges.values())),
            "{:,}".format(k[0]),
        )
    console.print()
    console.print(graphtable)

    table = Table(
        title="Benchmarks (max of five trials, times in \xb5s/execution)",
        box=rich.box.MARKDOWN,
    )
    table.add_column("Graph")
    for mod_name in IMPORTS:
        table.add_column(mod_name, justify="right")
    for g, (num, exclude_list) in GRAPH_FILES.items():
        to_output = [g]
        for mod_name in IMPORTS:
            if mod_name not in exclude_list:
                to_output.append(
                    "{:,}".format(
                        round(
                            run_time_test(
                                TimeTest(f"from {mod_name} import reachable", g),
                                num,
                            )
                            * 1_000_000
                        )
                    )
                )
            else:
                to_output.append("-")
        table.add_row(*to_output)
    console.print()
    console.print(table)
