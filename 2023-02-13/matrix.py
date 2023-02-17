# matrix.py

"""Solution to David Amos's weekly coding challenge for 2023-02-13:
    https://discourse.davidamos.dev/t/flight-inference/135
"""

from sys import argv

import numpy as np

from _resources import DirectedGraph, format_answer


def reachable(dgraph: DirectedGraph) -> dict[str, list[str]]:
    """Find which destinations are reachable from a given starting point."""
    num_vert = len(dgraph.vertices)
    incidence_mat = np.array(
        [
            [
                1
                if (dgraph.vertices[k] in dgraph.edges[dgraph.vertices[j]]) or (j == k)
                else 0
                for k in range(num_vert)
            ]
            for j in range(num_vert)
        ],
        np.int64,
    )
    old_reachable = np.zeros((num_vert, num_vert), np.int64)
    reachable_mat = incidence_mat
    while np.count_nonzero(reachable_mat) != np.count_nonzero(old_reachable):
        old_reachable = reachable_mat
        reachable_mat = reachable_mat @ incidence_mat != 0
    return {
        dgraph.vertices[j]: list(
            dgraph.vertices[k]
            for k in range(num_vert)
            if reachable_mat[j, k] != 0 and j != k
        )
        for j in range(num_vert)
    }


if __name__ == "__main__":
    if len(argv) > 1:
        data = DirectedGraph.read_file(argv[1])
        output = reachable(data)
        print(format_answer(output))
