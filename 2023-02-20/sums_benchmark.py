"""Time the various functions in `sums.py`."""

import timeit
from typing import Final

NUM_REPEAT: Final[dict[int, int]] = {
    14: 10_000,
    -15: 10_000,
    120: 100,
    0: 10_000,
}

RANGES: Final[list[tuple[int, int]]] = [(-3, 3), (0, 8), (-20, 20)]
RANGE_REPEATS: Final[int] = 1_000

FUNC_NAMES: Final[list[str]] = [
    "loop",
    "listcomp",
    "recursive",
    "cached_recursive",
    "gauss_sum",
]
results: dict[str, dict[int, float]] = {k: {} for k in FUNC_NAMES}
range_results: dict[str, dict[tuple[int, int], float]] = {k: {} for k in FUNC_NAMES}

for func in FUNC_NAMES:
    for num, repeats in NUM_REPEAT.items():
        t = timeit.Timer(f"value = {func}({num})", setup=f"from sums import {func}")
        results[func][num] = max(
            k / repeats * 1_000_000 for k in t.repeat(number=repeats)
        )
    for r in RANGES:
        t = timeit.Timer(
            f"value = [{func}(k) for k in range({r[0]}, {r[1]})]",
            setup=f"from sums import {func}",
        )
        range_results[func][r] = max(
            k / RANGE_REPEATS * 1_000_000 for k in t.repeat(number=RANGE_REPEATS)
        )
range_headers_raw = [f"`range({r[0]}, {r[1]})`" for r in RANGES]
range_header_max = max(len(k) for k in range_headers_raw)
range_headers = [
    ("{:>" + str(range_header_max) + "}").format(k) for k in range_headers_raw
]

max_f_len = max(len(k) for k in FUNC_NAMES)
func_header = "Function"
func_header = func_header + " " * (max_f_len + 2 - len(func_header))
print(
    f"| {func_header} | "
    + " | ".join(f"{str(num):>8}" for num in NUM_REPEAT.keys())
    + " | "
    + " | ".join(range_headers)
    + " | "
)
print(
    "| :"
    + "-" * (len(func_header) - 1)
    + " "
    + "| -------: " * len(NUM_REPEAT.keys())
    + ("| " + "-" * (2 + range_header_max - 3) + ": ") * len(RANGES)
    + "|"
)
for func, times in results.items():
    func_name = "`" + func + "`" + " " * (len(func_header) - len(func) - 2)
    print(
        f"| {func_name} | "
        + " | ".join(f"{v:0.3f} \xb5s" for v in times.values())
        + " | "
        + " | ".join(
            " " * (range_header_max - len(s := f"{v:4.3f} \xb5s")) + s
            for v in range_results[func].values()
        )
        + " |"
    )
