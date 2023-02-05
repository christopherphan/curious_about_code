"""Test the Rust version of my program."""

import datetime
import subprocess
from typing import Final

from fifteenpuzzle import (as_puzzle_input, possible_next_moves, scramble,
                           tile_to_move)
from integerpermutations import IDENTITY, IntegerPermutation

RUST_COMMAND: Final[str] = "../rust_2023-01-29/target/release/rust_2023-01-29"


def run_test() -> bool:
    """Create a puzzle then run the rust solver and check the solution."""
    # Make a puzzle
    puzzle = scramble(IDENTITY)
    # Save the puzzle
    filename = f"_puzzle_{datetime.datetime.now():%Y%m%d%H%M%S}"
    with open(filename, "wt") as outfile:
        outfile.write(as_puzzle_input(puzzle))
    print(f"Puzzle saved to {filename}")
    # Run rust solver
    print("Running rust solver")
    rust_output = subprocess.run(
        [RUST_COMMAND, filename], capture_output=True, text=True
    )
    rust_output_filename = filename + "_rust_output"
    print(f"Rust solver done. Output saved to {rust_output_filename}")
    with open(rust_output_filename, "wt") as outfile:
        outfile.write(rust_output.stdout)
    # Verify solution
    soln = [
        int(k.strip())
        for k in rust_output.stdout.split("Solution:,")[1].replace("\n", "").split(",")
    ]
    if check_soln(puzzle, soln):
        print("Solution is correct")
        return True
    else:
        print("Solution is incorrect")
        return False


def check_soln(puzzle: IntegerPermutation, soln: list[int]) -> bool:
    """Check the solution."""
    for k in soln:
        poss_moves = {
            tile_to_move(puzzle, key): value
            for key, value in possible_next_moves(puzzle).items()
        }
        if k in poss_moves:
            puzzle @= poss_moves[k]
        else:
            return False
    return puzzle == IDENTITY


if __name__ == "__main__":
    num_correct = 0
    for k in range(50):
        print(f"Running test {k}:")
        if run_test():
            num_correct += 1
        print("\n\n")
    print(f"----\nTotal tests correct: {num_correct} / 50")
