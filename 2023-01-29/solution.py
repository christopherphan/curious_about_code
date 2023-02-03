"""
Solution to David Amos's "Curious About Code" puzzle for 2023-01-29:
https://discourse.davidamos.dev/t/the-fifteen-puzzle/124
"""

from sys import argv
from typing import Final

from fifteenpuzzle import (manhattan_distance, read_arrangment,
                           valid_permutation)

SAMPLE_PART1: Final[
    str
] = """\
15 14 13 12
11 10 9 8
7 6 5 4
3 2 1 E"""

if len(argv) > 1:
    with open(argv[1], "rt") as infile:
        puzzle_input = infile.read()
else:
    puzzle_input = SAMPLE_PART1
perm = read_arrangment(puzzle_input)
print(f"Puzzle:\n{puzzle_input}\n")
print(f"Positions -> tiles: {perm}")
print(f"Pieces -> tiles: {~perm}")
print(f"Pairity: {(~perm).pairity}")
print(
    "Manhattan distance of empty square from bottom-right corner: "
    + str(manhattan_distance((~perm)(16)))
)
print("\nPART 1:\n------")
print(f"Valid arrangment: {valid_permutation(perm)}")
