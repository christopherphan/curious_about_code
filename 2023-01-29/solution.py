"""
Solution to David Amos's "Curious About Code" puzzle for 2023-01-29:
https://discourse.davidamos.dev/t/the-fifteen-puzzle/124
"""

from sys import argv
from textwrap import fill
from typing import Final

import bruteforce
from fifteenpuzzle import (as_puzzle_input, manhattan_distance,
                           read_arrangement, valid_permutation)
from integerpermutations import IntegerPermutation

PROBLEM_1: Final[
    str
] = """\
15 14 13 12
11 10 9 8
7 6 5 4
3 2 1 E"""

PROBLEM_2: Final[
    str
] = """\
12 1 2 15
11 6 5 8
7 10 9 4
E 13 14 3"""


def describe_puzzle(perm: IntegerPermutation):
    """Describe the puzzle."""
    print(f"Puzzle:\n{as_puzzle_input(perm)}\n")
    print(f"Positions -> tiles: {perm}")
    print(f"Tiles -> positions: {~perm}")
    print(f"Pairity: {(~perm).pairity}")
    print(
        "Manhattan distance of empty square from bottom-right corner: "
        + str(manhattan_distance((~perm)(16)))
    )


if len(argv) > 1:
    with open(argv[1], "rt") as infile:
        puzzles = [read_arrangement(infile.read())]
else:
    puzzles = [read_arrangement(k) for k in [PROBLEM_1, PROBLEM_2]]

if len(puzzles) == 1:
    describe_puzzle(puzzles[0])
print("\nPART 1:\n------")
if len(puzzles) == 2:
    describe_puzzle(puzzles[0])
valid = valid_permutation(puzzles[0])
print(f"Valid arrangment: {valid}")

if len(puzzles) == 2 or valid:
    print("\nPART 2:\n------")
    puz = puzzles[-1]
    if len(puzzles) == 2:
        describe_puzzle(puz)
    if valid_permutation(puz):
        moves, tiles = bruteforce.solve(puz)
        print(
            "\n"
            + fill("Solution (sequence of tiles): " + ", ".join(str(k) for k in tiles))
        )
        print(
            "\n" + fill("Solution (sequence of slides): " + ", ".join(k for k in moves))
        )
    else:
        print("Not a valid puzzle layout.")
