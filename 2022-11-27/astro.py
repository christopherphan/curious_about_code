#!/usr/bin/env python3

"""
astro.py: Solve the "Astronaut logic" puzzle.

This is a simple script to solve the "Astronaut logic" puzzle at
<https://discourse.davidamos.dev/t/astronaut-logic/63>
"""

from calendar import month_name
from collections.abc import Sequence
from itertools import permutations
from typing import Final

__author__ = "Christopher Phan <chrisphan.com>"
__copyright__ = "Copyright 2022, Christopher Phan"
__license__ = "MIT"


ASTRONAUTS: Final[list[str]] = ["Delia", "Mercedes", "Seth", "Wade"]
MISSIONS: Final[list[str]] = ["AV-435", "CR-260", "PR-97", "ZF-15"]


def format_schedule(astro_order: Sequence[str], miss_order: Sequence[str]) -> str:
    """Output a schedule in the required format."""
    return "\n".join(
        f"{astro} {month_name[idx + 1]} {miss}"
        for idx, (astro, miss) in enumerate(zip(astro_order, miss_order))
    )


print(
    "\n\n".join(
        format_schedule(a, m)
        for m in permutations(MISSIONS)
        for a in permutations(ASTRONAUTS)
        if (  # Condition 1
            (target := {"Mercedes", "ZF-15"}) == {a[0], m[3]} or target == {a[3], m[0]}
        )
        and m[3] == "CR-260"  # Condition 2
        and a[m.index("PR-97")] == "Wade"  # Condition 3
        and len({a[1], a[m.index("ZF-15")], "Wade"}) == 3  # Condition 4
        and a.index("Seth") > a.index("Delia")  # Condition 5
    )
)
