"""Solve a 15 puzzle by brute force."""
# I am not sure this is possible, but let's try!

from __future__ import annotations

from dataclasses import dataclass
from sys import argv

from fifteenpuzzle import (as_puzzle_input, possible_next_moves,
                           read_arrangement, scramble, tile_to_move,
                           valid_permutation)
from integerpermutations import IDENTITY, IntegerPermutation


def position_coordinates(val: int) -> tuple[int, int]:
    """Return the coordinates for a fifteen puzzle position."""
    if val < 1 or val > 16:
        raise ValueError(f"Invalid position {val}")
    return (val - 1) // 4, (val - 1) % 4


def manhattan_distance(a: int, b: int) -> int:
    """Return the manhattan distance between positions a and b."""
    ax, ay = position_coordinates(a)
    bx, by = position_coordinates(b)
    return abs(ax - bx) + abs(ay - by)


# Not sure the best metric
def score(arr: IntegerPermutation) -> int:
    """Evaluate how close the puzzle is to solved."""
    return sum(manhattan_distance((~arr)(k), k) for k in range(1, 17))


@dataclass
class PositionData:
    """Store information about an arrangement."""

    score: int
    adjacent: dict[str, tuple[IntegerPermutation, int]]
    shortest_route: tuple[str, list[int]]
    exhausted: bool

    @classmethod
    def from_perm(
        cls: type[PositionData],
        perm: IntegerPermutation,
        route: tuple[str, list[int]] | None = None,
    ) -> PositionData:
        """Make a PositionData object from an arrangement."""
        if route is None:
            route = ("", [])
        return cls(
            score(perm),
            {
                key[0]: (perm @ value, tile_to_move(perm, key[0]))
                for key, value in possible_next_moves(perm).items()
            },
            route,
            False,
        )


def min_score(data: dict[IntegerPermutation, PositionData]) -> IntegerPermutation:
    """Return the best-scoring permutation explored so far."""
    return min(
        (perm for perm in data.keys() if not data[perm].exhausted),
        key=lambda perm: data[perm].score,
    )


def step(data: dict[IntegerPermutation, PositionData]):
    """Perform one iteration of my brute-force algorithm, modifying data in-place."""
    next_perm = min_score(data)
    for direction, (perm, tile) in data[next_perm].adjacent.items():
        new_route = (
            data[next_perm].shortest_route[0] + direction,
            data[next_perm].shortest_route[1] + [tile],
        )
        if perm not in data:
            data[perm] = PositionData.from_perm(perm, new_route)
        elif len(new_route[0]) < len(data[perm].shortest_route[0]):
            data[perm].shortest_route = new_route
    data[next_perm].exhausted = True


def solve(puzzle: IntegerPermutation) -> tuple[str, list[int]]:
    """Solve the puzzle and return the list of moves."""
    data = {puzzle: PositionData.from_perm(puzzle)}
    while IDENTITY not in data:
        step(data)
    return data[IDENTITY].shortest_route


if __name__ == "__main__":
    if len(argv) > 1:
        with open(argv[1], "rt") as infile:
            puzzle = read_arrangement(infile.read())
    else:
        puzzle = scramble(IDENTITY)

    if not valid_permutation(puzzle):
        raise ValueError("Not a valid puzzle layout.")
    print(as_puzzle_input(puzzle))
    print("\n---\n")
    print("\n".join(str(k) for k in solve(puzzle)[1]))
