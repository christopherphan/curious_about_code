# Solution to the "Validating Pilish" puzzle

- Puzzle at: <https://discourse.davidamos.dev/t/validating-pilish/39>

- `pilish.py`: Script to validate a text file to determine if it's valid pilish

  - Usage: `./pilish.py filename`

  - Runs in Python 3.9+ with no dependencies (`requirements.txt` gives the dev
    environment I use)

- `make_pilish.jl`: Program to produce a pilish "poem" out of some public domain
  texts. Outputs to the standard output.

- `pilish_*.txt`: Some "poems" produced by `make_pilish.jl`.
