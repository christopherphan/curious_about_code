"""
Solution to "Perfectly Squared Squares" puzzle on David Amos's "Curious About Code"
site: <https://discourse.davidamos.dev/t/perfectly-squared-squares/115>
"""

from __future__ import annotations

from collections.abc import Iterator, Sequence
from dataclasses import dataclass
from sys import argv

import matplotlib.patches as mpatches


@dataclass
class Square:
    top_left_corner: tuple[int, int]
    length: int
    parent: Square | None = None
    children: list[Square] | None = None

    def as_mpatch(
        self: Square,
        zero_point: tuple[int | float, int | float] = (0, 0),
        top_down: bool = False,
        **kwargs,
    ) -> mpatches.Rectangle:
        """Return a matplotlib patch."""
        return mpatches.Rectangle(
            xy=(
                float(zero_point[0] + self.top_left_corner[0]),
                float(zero_point[1] + (-1) if top_down else 1)
                * self.top_left_corner[1],
            ),
            width=float(self.length),
            height=float(self.length),
            rotation_point=0,
            label=self.length,
            **kwargs,
        )

    def on_right(self: Square, length: int, v_offset: int = 0) -> Square:
        """Return a new square to the right of this square."""
        return self.__class__(
            top_left_corner=(
                self.top_left_corner[0] + self.length,
                self.top_left_corner[1] + v_offset,
            ),
            length=length,
            parent=self,
        )

    def add_on_right(self: Square, length: int, v_offset: int = 0) -> Square:
        new_square = self.on_right(length, v_offset)
        if self.children is None:
            self.children = [new_square]
        else:
            self.children.append(new_square)
        return new_square

    @classmethod
    def from_tuple(
        cls: type[Square],
        seq: Sequence[int],
        base_square: Square | None = None,
        v_offset: int = 0,
    ) -> list[Square]:
        """Return a list of Squares given a sequence of ints."""
        ret_list: list[Square] = []
        for idx, item in enumerate(seq):
            if idx == 0:
                if base_square is not None:
                    ret_list.append(base_square.add_on_right(item, v_offset))
                else:
                    ret_list.append(Square((0, v_offset), item))
            else:
                ret_list.append(ret_list[-1].add_on_right(item))
        return ret_list

    def contains(self: Square, pos: tuple[int | float, int | float]) -> bool:
        return (0 <= pos[0] - self.top_left_corner[0] < self.length) and (
            0 <= pos[1] - self.top_left_corner[1] < self.length
        )

    @property
    def _right_edge(self: Square) -> Iterator[tuple[int, int]]:
        return (
            (self.top_left_corner[0] + self.length, self.top_left_corner[1] + k)
            for k in range(0, self.length)
        )

    @property
    def all_from_here(self: Square) -> Iterator[Square]:
        yield self
        if self.children is not None:
            for k in self.children:
                for k2 in k.all_from_here:
                    yield k2

    @property
    def top_ancestor(self: Square) -> Square:
        k = self
        while k.parent is not None:
            k = k.parent
        return k

    def at_location(self: Square, pos: tuple[int, int]) -> Square | None:
        if self.parent is None:
            for s in self.all_from_here:
                if s.contains(pos):
                    return s
            return None
        else:
            return self.top_ancestor.at_location(pos)

    def free_on_right_edge(self: Square) -> Iterator[tuple[int, int]]:
        for k in self._right_edge:
            if self.at_location(k) is None:
                yield k
