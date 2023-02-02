"""
Solution to Part 1 of this puzzle:
https://discourse.davidamos.dev/t/the-fifteen-puzzle/124
"""

from sys import argv
from typing import Final

from integerpermutations import IntegerPermutation


def read_arrangment(text: str) -> IntegerPermutation:
    """Read the arrangment. The empty space is assigned zero."""
    return IntegerPermutation(
        {
            idx + 1: (16 if val == "E" else int(val))
            for idx, val in enumerate(
                [k.strip() for k in text.replace("\n", " ").split(" ")]
            )
        }
    )


def manhattan_distance(x: int) -> int:
    """Return the Manhattan distance from square position x to position 16."""
    if x < 1 or x > 16:
        raise ValueError(f"Invalid position {x}")
    return abs(4 * ((x - 1) // 4 + 1) - x) + abs(3 - (x - 1) // 4)


def valid_permutation(x: IntegerPermutation) -> bool:
    """Return true if x represents a valid arrangement of the 15 puzzle."""
    return not bool((x.pairity + manhattan_distance((~x)(16))) % 2)


def as_puzzle_input(x: IntegerPermutation) -> str:
    """Return as text in the style of the puzzle input."""
    return "\n".join(
        " ".join(str(w) if (w := x(4 * k + j)) != 16 else "E" for j in range(1, 5))
        for k in range(4)
    )


if __name__ == "__main__":
    SAMPLE: Final[
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
        puzzle_input = SAMPLE
    perm = read_arrangment(puzzle_input)
    print(f"Puzzle:\n{puzzle_input}")
    print(f"Positions -> pieces: {perm}")
    print(f"Pieces -> positions: {~perm}")
    print(f"Valid arrangment: {valid_permutation(perm)}")
