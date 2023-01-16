"""Find the order of a squaring input file, and determine if there is a common factor."""

from math import gcd
from sys import argv

if len(argv) == 1:
    print(f"Usage: {argv[0]} filename")
else:
    values: list[int] = []
    with open(argv[1], "rt") as infile:
        for line in infile:
            values += [
                int(k) for k in line.replace("(", "").replace(")", "").split(",")
            ]
    print(f"Order: {len(values)}")
    print(f"GCD: {gcd(*values)}")
