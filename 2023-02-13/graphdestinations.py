# graphdestinations.py

"""Solution to David Amos's weekly coding challenge for 2023-02-13:
    https://discourse.davidamos.dev/t/flight-inference/135
"""

from collections import defaultdict
from sys import argv

from _resources import DirectedGraph, format_answer


def reachable(dgraph: DirectedGraph) -> dict[str, list[str]]:
    """Find which destinations are reachable from a given starting point."""
    output: dict[str, list[str]] = defaultdict(list)
    for origin in dgraph.vertices:
        visited = {vertex: False for vertex in dgraph.vertices}
        visited[origin] = True
        places_to_go: list[str] = [origin]
        while places_to_go:
            v = places_to_go.pop()
            for v2 in dgraph.edges[v]:
                output[origin].append(v2)
                if not visited[v2]:
                    if v2 in output:
                        output[origin].extend(output[v2])
                    else:
                        places_to_go.append(v2)
            visited[v] = True
    return {v: list(set([k for k in output[v] if k != v])) for v in dgraph.vertices}


if __name__ == "__main__":
    if len(argv) > 1:
        data = DirectedGraph.read_file(argv[1])
        output = reachable(data)
        print(format_answer(output))
