"""Bijections on the integers that fix all but a finite number of elements."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from functools import cached_property


def _not_injective_msg(in_1: int, in_2: int, out: int) -> str:
    """Provide an error message when the function is not injective."""
    return f"Not one-to-one, as {in_1} and {in_2} both map to {out}."


class IntegerPermutation:
    """A bijection on the integers that fixes all but a finite number of elements."""

    def __init__(self: IntegerPermutation, mapping: Mapping[int, int]) -> None:
        """Initialize the permutation."""
        self._mapping: dict[int, int] = dict()
        self._reverse_mapping: dict[int, int] = dict()
        for key, value in sorted(mapping.items()):
            for k, v in {"key": key, "value": value}.items():
                if not isinstance(v, int):
                    raise TypeError(f"{k} {v!r} is not an integer.")
            if key != value:
                if value in self._reverse_mapping:
                    raise ValueError(
                        _not_injective_msg(key, self._reverse_mapping[value], value)
                    )
                self._mapping[key] = value
                self._reverse_mapping[value] = key
        # final bijection check
        for v in self._reverse_mapping:
            if v not in self._mapping:
                raise ValueError(_not_injective_msg(v, self._reverse_mapping[v], v))

    def __call__(self: IntegerPermutation, value: int) -> int:
        """Evaluate self on the provided value."""
        if not isinstance(value, int):
            raise TypeError(f"{value} is not an integer.")
        if value in self._mapping:
            return self._mapping[value]
        else:
            return value

    def __repr__(self: IntegerPermutation) -> str:
        """Return repr(self)."""
        return f"{self.__class__.__name__}({self._mapping!r})"

    def __str__(self: IntegerPermutation) -> str:
        """Return str(self)."""
        if self.cycle_decomposition:
            return " ".join(repr(k) for k in self.cycle_decomposition)
        else:
            return "[0]"

    @cached_property
    def _underlying_frozenset(self: IntegerPermutation):
        """Return a frozenset containing key-value pairs."""
        return frozenset((key, value) for key, value in self._mapping.items())

    def __hash__(self: IntegerPermutation) -> int:
        """Return hash(self)."""
        return hash(self._underlying_frozenset)

    def __eq__(self: IntegerPermutation, other) -> bool:
        """Return true if self == other."""
        if isinstance(other, IntegerPermutation):
            return self._underlying_frozenset == other._underlying_frozenset
        else:
            return NotImplemented

    def __matmul__(self: IntegerPermutation, other):
        """Return the composition of self after other."""
        if isinstance(other, IntegerPermutation):
            return self.__class__(
                self._mapping
                | {key: self(value) for key, value in other._mapping.items()}
            )
        else:
            return NotImplemented

    @cached_property
    def _inverse(self: IntegerPermutation) -> IntegerPermutation:
        """Return the (compositional) inverse of self."""
        return self.__class__(self._reverse_mapping)

    def __invert__(self: IntegerPermutation) -> IntegerPermutation:
        """Return the (compositional) inverse of self, ``~self``."""
        return self._inverse

    @classmethod
    def cycle(cls: type[IntegerPermutation], vals: Sequence[int]) -> IntegerPermutation:
        """Construct a permutation out of the cycle given by vals."""
        val_list = list(vals)
        return cls({k: v for k, v in zip(val_list, val_list[1:] + val_list[:1])})

    @classmethod
    def cycle_sequence(
        cls: type[IntegerPermutation], cycles: Sequence[Sequence[int]]
    ) -> IntegerPermutation:
        """Construct a permutation out a sequence of cycles."""
        ret_val = cls({})
        for k in cycles:
            ret_val @= cls.cycle(k)
        return ret_val

    @cached_property
    def cycle_decomposition(self: IntegerPermutation) -> list[list[int]]:
        """Decompose self into a set of disjoint cycles."""
        cycle_dict: dict[int, list[int]] = {}
        ret_val: list[list[int]] = []
        for key in self._mapping.keys():
            if key not in cycle_dict:
                new_cycle = [key]
                u = self(key)
                while u != key:
                    new_cycle.append(u)
                    u = self(u)
                ret_val.append(new_cycle)
                for u in new_cycle:
                    cycle_dict[u] = new_cycle
        return ret_val

    @cached_property
    def pairity(self: IntegerPermutation) -> int:
        """Return 0 if self is an even permutation, 1 if self is an odd permutation."""
        return len([k for k in self.cycle_decomposition if len(k) % 2 == 0]) % 2


if __name__ == "__main__":
    a = IntegerPermutation({1: 5, 5: 7, 7: 3, 3: 1, 10: 9, 9: 10, 8: 8})
    b = IntegerPermutation({1: 5, 5: 7, 7: 3, 3: 1, 10: 9, 9: 10})
    for k in range(11):
        print(k, a(k))
    print(hash(a))
    print(hash(b))
    print(a == b)
    c = IntegerPermutation({4: 7, 7: 9, 9: 4})
    d = a @ c
    for k in range(10):
        print(f"{k} -> {c(k)} -> {a(c(k))}\t", (d)(k))
    e = IntegerPermutation.cycle([4, 3, 9, 2])
    f = IntegerPermutation.cycle_sequence(
        [[5, 2, 3], [3, 4, 1], [11, 8, 7], [7, 10, -4]]
    )
    g = IntegerPermutation.cycle_sequence([[51, 2], [3, -104], [5, 0]])
    print("----")
    for v, w in zip("acdefg", [a, c, d, e, f, g]):
        print(f"{v} = " + repr(w))
        print(w)
        print(w.pairity)
        print(f"~{v} = " + repr(~w))
        print(~w)
        print(~w.pairity)
        print(f"{v} @ ~{v}: {w @ ~w}")
