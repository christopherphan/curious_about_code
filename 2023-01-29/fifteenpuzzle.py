"""Validate 15 puzzle arrangements."""


from random import choice
from sys import argv
from typing import Final

from integerpermutations import IntegerPermutation

VALID_MOVES: Final[frozenset[IntegerPermutation]] = frozenset(
    # Represents the valid transpositions of the _positions_ (not tiles)
    # in the puzzle (assuming that one of the two positions swapped is
    # the empty tile). Right-multiplication by a valid move represents
    # carrying out the swap on the puzzle arrangement.
    [IntegerPermutation.transposition(j, j + 4) for j in range(1, 5)]
    + [IntegerPermutation.transposition(j, j + 4) for j in range(9, 13)]
    + [IntegerPermutation.transposition(j, j + 1) for j in range(1, 14, 4)]
    + [IntegerPermutation.transposition(j, j + 1) for j in range(3, 16, 4)]
)


def read_arrangement(text: str) -> IntegerPermutation:
    """
    Read the arrangement and return a permutation mapping positions to tiles.

    The empty space is considered tile 16. The positions are indexed by the
    corresponding tile in the solved puzzle.
    """
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


def empty_position(arrangement: IntegerPermutation) -> int:
    """Return the position with no tile."""
    return (~arrangement)(16)


# An arrangement is valid if the pairty of the representative permutation and the
# pairity of the Manhattan distance from empty position to the bottom right corner
# agree.


def valid_permutation(perm: IntegerPermutation) -> bool:
    """
    Return true if ``perm`` represents a valid arrangement of the 15 puzzle.

    :param perm: A permutation that maps each position to the tile occupying it.
    :type perm: IntegerPermutation
    """
    return all(k < 17 and k > 0 for k in perm.unfixed) and not bool(
        ((~perm).pairity + manhattan_distance(empty_position(perm))) % 2
    )


def as_puzzle_input(perm: IntegerPermutation) -> str:
    """Return as text in the style of the puzzle input."""
    return "\n".join(
        " ".join(str(w) if (w := perm(4 * k + j)) != 16 else "E" for j in range(1, 5))
        for k in range(4)
    )


def possible_next_moves(
    arrangement: IntegerPermutation,
) -> dict[str, IntegerPermutation]:
    """Return a the possible next moves given a puzzle arrangement."""
    empty_pos = empty_position(arrangement)
    ret_val: dict[str, IntegerPermutation] = {}
    if empty_pos > 4:
        # Move empty square up
        ret_val["up"] = IntegerPermutation.transposition(empty_pos, empty_pos - 4)
    if empty_pos < 13:
        # Move empty square down
        ret_val["down"] = IntegerPermutation.transposition(empty_pos, empty_pos + 4)
    if (empty_pos % 4) != 0:
        # move empty square right
        ret_val["right"] = IntegerPermutation.transposition(empty_pos, empty_pos + 1)
    if (empty_pos % 4) != 1:
        # move empty square left
        ret_val["left"] = IntegerPermutation.transposition(empty_pos, empty_pos - 1)
    return ret_val


def tile_to_move(arrangement: IntegerPermutation, direction: str) -> int:
    """Return the label on the tile that is moved when going a certain direction."""
    if direction:
        parsed_direction = direction[0].lower()
    else:
        raise ValueError("Empty direction")
    empty_pos = empty_position(arrangement)
    if parsed_direction == "u" and empty_pos > 4:
        return arrangement(empty_pos - 4)
    elif parsed_direction == "d" and empty_pos < 13:
        return arrangement(empty_pos + 4)
    elif parsed_direction == "l" and empty_pos % 4 != 1:
        return arrangement(empty_pos - 1)
    elif parsed_direction == "r" and empty_pos % 4 != 0:
        return arrangement(empty_pos + 1)
    else:
        raise ValueError(f"Invalid direction {direction!r}")


def _game_status(arrangement: IntegerPermutation, disp_perm: bool = False) -> str:
    """Return the board and if the puzzle is solved."""
    return (
        (f"E at {empty_position(arrangement)}\n" if disp_perm else "")
        + "\n".join(
            " ".join(
                f"{w:2d}" if (w := arrangement(4 * k + j)) != 16 else " E"
                for j in range(1, 5)
            )
            for k in range(4)
        )
        + ("" if arrangement.unfixed else "\n\nPUZZLE IS SOLVED!")
        + (f"\n{arrangement}" if disp_perm else "")
    )


def scramble(
    arrangement: IntegerPermutation, num_moves: int = 256
) -> IntegerPermutation:
    """Apply random moves."""
    current = arrangement
    for _ in range(num_moves):
        current @= choice(list(possible_next_moves(current).values()))
    return current


def play_puzzle(arrangement: IntegerPermutation | None = None) -> None:
    """Present iteractive game."""
    if arrangement is not None and not valid_permutation(arrangement):
        raise ValueError(
            "Permutation does not represent a valid arrangement of the fifteen puzzle."
        )
    if arrangement is None:
        current = IntegerPermutation({})
        rando = input("Scramble pieces (Y/N)? ").strip()
        if not (rando and rando.upper()[0] == "N"):
            current = scramble(current)
    else:
        current = arrangement
    disp = input("Display permutations (Y/N)? ").strip()
    disp_perm = bool(disp) and disp.upper()[0] == "Y"
    print(_game_status(current, disp_perm))
    moved: IntegerPermutation | None
    while k := input("Enter move (U, D, L, R) or a blank input to exit: ").strip():
        moved = None
        pnm = possible_next_moves(current)
        for key, value in pnm.items():
            if k[0].lower() == key[0].lower():
                current @= value
                moved = value
                break
        if moved is None:
            print("Invalid move.")
        elif disp_perm:
            print(f"This move: {moved}")
        print(_game_status(current, disp_perm))


if __name__ == "__main__":
    if len(argv) > 1:
        with open(argv[1], "rt") as infile:
            play_puzzle(read_arrangement(infile.read()))
    else:
        play_puzzle()
