import random
from typing import Final

NUM_ROWS: Final[int] = 20
NUM_COLS: Final[int] = 20

all_locations = [(j, k) for j in range(NUM_ROWS) for k in range(NUM_COLS)]

mine_loc = random.sample(all_locations, 40)

print(
    "\n".join(
        "".join(("*" if (row, col) in mine_loc else ".") for col in range(NUM_COLS))
        for row in range(NUM_ROWS)
    )
)
