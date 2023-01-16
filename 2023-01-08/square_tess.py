"""
Solution to "Perfectly Squared Squares" puzzle on David Amos's "Curious About Code"
site: <https://discourse.davidamos.dev/t/perfectly-squared-squares/115>
"""

from __future__ import annotations

import json
import logging
from collections.abc import Iterator, Sequence
from functools import cached_property
from sys import argv

import matplotlib.patches as mpatches
import matplotlib.pyplot as plt


class RootNode:
    """Class for the root of an attempted tesselation."""

    def __init__(self: RootNode) -> None:
        """Initialize object."""
        self.children: list[SquareNode] = []  # the squares touching the left edge
        self._top_row_complete = False
        self._y = 0
        self._x = 0

    @property
    def descendents(self: RootNode) -> Iterator[SquareNode]:
        """Return all decendents."""
        for k in self.children:
            yield k
            for u in k.descendents:
                yield u

    def _find_which(self: RootNode, pos: tuple[int, int]) -> SquareNode | None:
        """Return the SquareNode (if any) that contains pos."""
        for d in self.descendents:
            if pos in d:
                return d
        return None

    @property
    def next_vert_offset(self: RootNode) -> int:
        """Return the y-coord for the top-left corner of the next square to attach."""
        return sum(k.length for k in self.children)

    def _add_square(self: RootNode, length: int) -> SquareNode:
        self.children.append(s := SquareNode(self, length, self.next_vert_offset))
        return s

    def __contains__(self: RootNode, pos: tuple[int | float, int | float]) -> bool:
        """Return True if pos inside any descendent."""
        return any(pos in d for d in self.descendents)

    @property
    def length(self: RootNode) -> int:
        """Return the length of the top row of squares."""
        if not self.children:
            return 0
        else:
            k = self.children[0]
            val = k.length
            while k.aligned_child is not None:
                k = k.aligned_child
                val += k.length
            return val

    @property
    def height(self: RootNode) -> int:
        """Return the sum of the lengths of squares on the left edge."""
        if not self.children:
            return 0
        else:
            return sum(k.length for k in self.children)

    @property
    def next_to_attach(self: RootNode) -> RootNode | SquareNode:
        """Find the square the next tuple will be attached to."""
        candidate = self
        for d in self.descendents:
            assert candidate.next_vert_offset is not None
            logging.debug(
                f"Candidate: {candidate}, abs NVO:"
                + f" {candidate.next_vert_offset + candidate._y}"
                + f"\tLooking at {d}, abs NVO: "
                + f"{dnvo + d._y if (dnvo:= d.next_vert_offset) is not None else None}"
            )
            if (
                (not self._top_row_complete or d._x + d.length < self.length)
                and ((v := d.next_vert_offset) is not None)
                and (
                    (v_diff := v + d._y - (candidate.next_vert_offset + candidate._y))
                    < 0
                    or (
                        v_diff == 0
                        and d._x + d.length < candidate._x + candidate.length
                    )
                )
            ):
                candidate = d
        logging.debug(f"Next to attach: {candidate}\n")
        return candidate

    def add_tuple(self: RootNode, seq: Sequence[int]) -> None:
        """Add the squares represented by a tuple."""
        k = self.next_to_attach
        for u in seq:
            if (w := k._add_square(u)) is None:
                raise ValueError(f"Can't attach {u} onto {k}")
            else:
                logging.info(f"Attached {w} onto {k}")
                k = w
        self._top_row_complete = True

    @property
    def valid_square(self: RootNode) -> bool:
        """Return True if this is a perfectly squared square."""
        return (
            self.height
            == self.length  # bonus problem input describes a non-square rectangle
            and len(set(d.length for d in self.descendents))
            == len(
                set(self.descendents)
            )  # Requirement that every square have a different size
            and self.next_to_attach == self  # No gaps inside
            and all(
                (u := d.bottom_right_corner)[0] <= self.length and u[1] <= self.length
                for d in self.descendents
            )  # squares don't spill outside area
        )

    def as_plt(self: RootNode, output_filename: str) -> None:
        """Create a matplotlib figure and save to file."""
        fig, ax = plt.subplots(figsize=[10, 10 * (self.height / self.length)])
        for d in self.descendents:
            ax.add_patch(
                d.as_mpatch(
                    zero_point=(0, self.length),
                    top_down=True,
                    edgecolor="k",
                    facecolor="None",
                )
            )
            pos = d.m_coord(zero_point=(0, self.length), top_down=True)
            ax.text(
                pos[0] + 0.5 * d.length,
                pos[1] + 0.5 * d.length,
                d.length,
                ha="center",
                va="center",
            )
        ax.set_xlim(-self.length * 0.01, self.length * 1.01)
        ax.set_ylim(-self.height * 0.01, self.height * 1.01)
        # Make axes and ticks invisible
        for k in ("top", "right", "left", "bottom"):
            ax.spines[k].set_color("None")
        plt.xticks([])
        plt.yticks([])
        fig.savefig(output_filename)


class SquareNode:
    """
    A single square in the tessleation.

    :param parent: The square that lies directly to the left of this square. Has type
                   ``RootNode`` if square is on the left edge.
    :type parent: SquareNode | RootNode

    :param length: The length of a side of the square.
    :type length: int

    :param vert_offset: If parent has type ``SquareNode``, the distance from the top
                        right corner of the parent and the top left corner of the
                        square. If parent has type ``RootNode``, the vertical position
                        of the top of the square.
    :type vert_offset: int
    """

    def __init__(
        self: SquareNode,
        parent: SquareNode | RootNode,
        length: int,
        vert_offset: int = 0,
    ) -> None:
        """Initialize object."""
        self.parent = parent
        self.length = length
        self.vert_offset = vert_offset
        self.children: list[SquareNode] = []
        self._next_vert_offset = 0

    @property
    def descendents(self: SquareNode) -> Iterator[SquareNode]:
        """Return an iterator for all squares descending from this one."""
        for kid in self.children:
            yield kid
            for d in kid.descendents:
                yield d

    @property
    def aligned_child(self: SquareNode) -> SquareNode | None:
        """Return the child with top flush with the top of this square, if it exists."""
        for k in self.children:
            if k.vert_offset == 0:
                return k
        return None

    @cached_property
    def root(self: SquareNode) -> RootNode:
        """Return the RootNode ancestor."""
        k = self.parent
        while not isinstance(k, RootNode):
            k = k.parent
        return k

    @cached_property
    def _x(self: SquareNode) -> int:
        if isinstance(p := self.parent, RootNode):
            return 0
        else:
            return p._x + p.length

    @cached_property
    def _y(self: SquareNode) -> int:
        return self.parent._y + self.vert_offset

    @cached_property
    def top_left_corner(self: SquareNode) -> tuple[int, int]:
        """Return the position of the top-left corner of the square."""
        return self._x, self._y

    @cached_property
    def bottom_right_corner(self: SquareNode) -> tuple[int, int]:
        """Return the position of the bottom-right corner of the square."""
        return self._x + self.length, self._y + self.length

    def m_coord(
        self: SquareNode,
        zero_point: tuple[int | float, int | float] = (0, 0),
        top_down: bool = False,
    ) -> tuple[float, float]:
        """Return coordinates for use in matplotlib."""
        if top_down:
            y_coord = float(zero_point[1] - self.bottom_right_corner[1])
        else:
            y_coord = float(zero_point[1] + self.top_left_corner[1])
        return (float(zero_point[0] + self.top_left_corner[0]), y_coord)

    def as_mpatch(
        self: SquareNode,
        zero_point: tuple[int | float, int | float] = (0, 0),
        top_down: bool = False,
        **kwargs,
    ) -> mpatches.Rectangle:
        """Return a matplotlib patch."""
        return mpatches.Rectangle(
            self.m_coord(zero_point, top_down),
            width=float(self.length),
            height=float(self.length),
            **kwargs,
        )

    def __contains__(self: SquareNode, pos: tuple[int | float, int | float]) -> bool:
        """Return true if pos is inside the square."""
        return (0 <= pos[0] - self.top_left_corner[0] < self.length) and (
            0 <= pos[1] - self.top_left_corner[1] < self.length
        )

    @property
    def next_vert_offset(self: SquareNode) -> int | None:
        """Return the highest point on the right edge not adjacent to another square."""
        while self._next_vert_offset < self.length:
            if (
                fw := self.root._find_which(
                    (self._x + self.length, self._y + self._next_vert_offset)
                )
            ) is None:
                return self._next_vert_offset
            else:
                self._next_vert_offset = fw._y + fw.length - self._y
        return None

    @property
    def has_room_on_right(self: SquareNode) -> bool:
        """Return True if another square can be attached on the right."""
        return (
            (self._y != 0 or self.aligned_child is not None)
            and (self._y == 0 or self._x + self.length < self.root.length)
            and self.next_vert_offset is not None
        )

    def _add_square(self: SquareNode, length: int) -> SquareNode | None:
        nvo = self.next_vert_offset
        if nvo is None:
            return None
        new_square = self.__class__(self, length, nvo)
        self.children.append(new_square)
        return new_square

    def __str__(self: SquareNode) -> str:
        """Return ``str(self)``."""
        return f"Square at {self.top_left_corner} with length {self.length}"


if __name__ == "__main__":
    if len(argv) == 1 or (len(argv) == 2 and "--debug" in argv):
        print(f"Usage: {argv[0]} filename [--debug]")
    else:
        if len(argv) > 2 and argv[2].strip() == "--debug":
            log_lev = logging.DEBUG
        else:
            log_lev = logging.INFO
        logging.basicConfig(
            format="%(levelname)s %(filename)s:%(lineno)d %(funcName)s"
            + " %(asctime)s: %(message)s",
            filename="square_tess.log",
            filemode="w",
            level=log_lev,
        )
        logging.info(f"Running command: {' '.join(argv)}")
        with open(argv[1], "rt") as infile:
            raw_data = infile.read()
        if raw_data[-1] == "\n":
            raw_data = raw_data[:-1]
        raw_data = (
            "[" + raw_data.replace("\n", ",").replace("(", "[").replace(")", "]") + "]"
        )
        data = json.loads(raw_data)
        tess = RootNode()
        for k in data:
            tess.add_tuple(k)
        if tess.valid_square:
            print("Perfectly squared square")
        else:
            print("Not a perfectly squared square")
        fig = tess.as_plt(argv[1] + ".svg")
