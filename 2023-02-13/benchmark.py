# benchmark.py

"""Perform benchmarks for David Amos's weekly coding challenge for 2023-02-13:
    https://discourse.davidamos.dev/t/flight-inference/135
"""

import timeit
from typing import Final, NamedTuple


class TimeTest(NamedTuple):
    import_str: str
    graph_file: str


def make_timer(tt: TimeTest) -> timeit.Timer:
    return timeit.Timer(
        "reachable(graph)",
        setup=tt.import_str
        + "\nfrom _resources import DirectedGraph"
        + f"\n\ngraph = DirectedGraph.read_file({tt.graph_file!r})",
    )


def run_time_test(tt: TimeTest, num_repeat: int) -> list[float]:
    t = make_timer(tt)
    return [k / num_repeat for k in t.repeat(number=num_repeat)]


if __name__ == "__main__":
    IMPORTS: Final[list[str]] = ["graphdestinations", "matrix", "matrix2"]
    GRAPH_FILES: Final[dict[str, tuple[int, list[str]]]] = {
        "flights1.txt": (10_000, []),
        "gistfile1.txt": (1_000, []),
        "super_example.txt": (1, ["matrix", "matrix2"]),
    }
    for mod_name in IMPORTS:
        for g, (num, exclude_list) in GRAPH_FILES.items():
            if mod_name not in exclude_list:
                print(
                    f"{mod_name} on {g}: "
                    + ", ".join(
                        f"{val*1_000_000:0.6f} \xb5s"
                        for val in run_time_test(
                            TimeTest(f"from {mod_name} import reachable", g), num
                        )
                    )
                )
