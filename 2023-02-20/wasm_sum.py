"""Load sums.wasm and execute."""
from sys import argv

import wasmtime.loader
import wsums

if len(argv) >= 2:
    for k in argv[1:]:
        try:
            v = int(k.strip())
            print(f"{v}: {wsums.ourfunc(v)}")
        except ValueError:
            print(f"Couldn't parse {k}.")
else:
    print(f"Usage: {argv[0]} numbers")
