#!/usr/bin/env python3

"""
pilish.py: Simple Python script to test of a text file is valid Pilish.

This script requires the file one-million.txt to be in the same directory. This file
is found at <https://github.com/eneko/Pi/blob/master/one-million.txt>
"""

from __future__ import annotations

from collections.abc import Iterator, Sequence
from sys import argv
from typing import Final, NamedTuple, Optional

__author__ = "Christopher Phan <chrisphan.com>"
__copyright__ = "Copyright 2022, Christopher Phan"
__license__ = "MIT"

DIGITS: Final[str] = "".join(str(k) for k in range(10))


def _read_digits() -> list[int]:
    """
    Read the file ``one-million.txt`` and return a list of digits of pi.

    The file ``one-million.txt`` can be found at
    ``https://github.com/eneko/Pi/blob/master/one-million.txt``.
    """
    outlist: list[int] = []
    start_read = False
    # one-million.txt = https://github.com/eneko/Pi/blob/master/one-million.txt
    with open("one-million.txt", "rt") as infile:
        for line in infile:
            if not start_read:
                if line.strip() == "3.":
                    start_read = True
            if start_read:
                for c in line:
                    if c in DIGITS:
                        outlist.append(int(c))
    return outlist


PI_DIG: Final[list[int]] = _read_digits()


def ordinal(k: int) -> str:
    """Return the number followed by the appropriate suffix: st, nd, rd, or th."""
    last_dig = k % 10
    last_2dig = k % 100
    if last_dig == 1 and last_2dig != 11:
        return f"{k}st"
    elif last_dig == 2 and last_2dig != 12:
        return f"{k}nd"
    elif last_dig == 3 and last_2dig != 13:
        return f"{k}rd"
    else:
        return f"{k}th"


class PiDigit(NamedTuple):
    """Represent a digit of pi."""

    digit: int
    pos: int

    @classmethod
    def list_report(cls: type[PiDigit], digits: Sequence[PiDigit]) -> str:
        """Return a string describing a sequence of PiDigit objects for use in output."""
        if len(digits) == 1:
            return f"{ordinal(digits[0].pos + 1)} digit of pi is {digits[0].digit}."
        else:
            conjunction = "and" if len(digits) == 2 else "through"
            return (
                f"{ordinal(digits[0].pos + 1)} {conjunction} {ordinal(digits[-1].pos + 1)}"
                + f" digits of pi are {''.join(str(k.digit) for k in digits)}."
            )


class WordLength(NamedTuple):
    """Represent a word in the input and its length."""

    word: str
    raw_length: int
    digits: list[int]
    pos: int

    # Recall, a word with < 10 digits corresponds to one digit of pi,
    # a word with 10 digits corresponds to a 0 as a digit of pi,
    # but any word > 10 digits corresponds to multiple digits of pi.
    #
    # For example, the word Pneumonoultramicroscopicsilicovolcanoconiosis
    # (which is 45 letters) corresponds to the digits 4 and 5 in pi.
    # The word Lopadotemachoselachogaleokranioleipsanodrimhypotrimmatosilphiokarabome-
    # litokatakechymenokichlepikossyphophattoperisteralektryonoptekephalliok-
    # igklopeleiolagoiosiraiobaphetraganopterygon (which has 183 letters--it's the name
    # of a fictional dish in an ancient Greek commedy, see Wikipedia) corresponds
    # to the digits 1, 8, and 3 in pi.

    @classmethod
    def measure(cls: type[WordLength], word: str, pos: int) -> WordLength:
        """Measure word and produce a WordLength object."""
        word_len = len([k for k in word if k.isalpha()])
        if word_len == 10:
            return cls(word, 10, [0], pos)
        else:
            return cls(word, word_len, [int(k) for k in str(word_len)], pos)


class PilishValidationResult(NamedTuple):
    """Represent a result of validation."""

    valid: bool
    fail_pos: Optional[int]
    input_val: Optional[WordLength]
    pi_digit: Optional[list[PiDigit]]

    @property
    def verbose(self: PilishValidationResult) -> str:
        """Return a verbose report of the result (for use in user output)."""
        if self.valid:
            return "Text is a pilish!"
        else:
            assert self.fail_pos is not None
            assert self.input_val is not None
            assert self.pi_digit is not None
            return (
                f"Error at position {self.fail_pos}:"
                + f' The word "{self.input_val.word}" has {self.input_val.raw_length}'
                + f" letters, but the {PiDigit.list_report(self.pi_digit)}"
            )


def pi_dig() -> Iterator[PiDigit]:
    """Generate the digits of pi."""
    pos = 0
    size = len(PI_DIG)
    while pos < size:
        yield PiDigit(PI_DIG[pos], pos)
        pos += 1


def generate_words(text: str) -> Iterator[WordLength]:
    """Generate WordLength objects for the words in text."""
    word_num = 0
    size = len(text)
    pos = 0
    to_return = ""
    while pos < size:
        # Anything that's not a letter or an apostrophe is considered whitespace
        if (current_chr := text[pos]).isalpha() or current_chr == "'":
            to_return += current_chr
        elif to_return != "":
            yield WordLength.measure(to_return, word_num)
            word_num += 1
            to_return = ""
        pos += 1
    # If we reach the end of ``text``, return whatever is in the ``to_return`` buffer
    # before ending.
    if to_return != "":
        yield WordLength.measure(to_return, word_num)


def validate(text: str) -> PilishValidationResult:
    """Determine if ``text`` is in Pilish."""
    digits = pi_dig()
    words = generate_words(text)
    for wl in words:
        corresponding_digits = [next(digits) for _ in range(len(wl.digits))]
        for j, k in zip(wl.digits, corresponding_digits):
            if j != k.digit:
                return PilishValidationResult(False, wl.pos, wl, corresponding_digits)
    return PilishValidationResult(True, None, None, None)


def test() -> None:
    """Test a few examples and print the verbose version of the reports."""
    print("Test:")
    for text in [
        # Example given in the challenge
        "\n".join(
            [
                "But a time I spent wandering in gloomy night;",
                "Yon tower, tinkling chimewise, loftily opportune.",
                "Out, up, and together came sudden to Sunday rite,",
                "The one solemnly off to correct plenilune.",
            ]
        ),
        # The first verse of "Not A Wake"
        "\n".join(
            [
                "Now I fall, a tired suburbian in liquid under the trees",
                "Drifting alongside forests simmering red in the twilight over Europe.",
                "So scream with the old mischief, ask me another conundrum",
                "About bitterness of possible fortunes near a landscape Italian.",
                "A little happiness may sometimes intervene but usually fades.",
                "A missionary cries, striving to understand worthless, tedious life.",
                "Monotony's lost amid ocean movements",
                "As the bewildered sailors hesitate. I become salt,",
                "Submerging people in dazzling oceans of enshrouded unbelief.",
                "Christmas ornaments conspire.",
                "Beauty is, somewhat inevitably now, both",
                "Feelings of faith and eyes of rationalism.",
            ]
        ),
        # Some examples I made
        "For I have a great reckoning: he should watch any shows streamed.",  # pass
        "For I have a great reckoning--he should think he'd delay, overhead.",  # pass
        "Now I will present a string that doesn't work.",  # "present" is too long
        "Now I show a great counterexample.",  # invalid example with a long word
        "This won't work at all.",  # invalid ex where the report has 1st
        "Counterexamples are fun.",  # invalid ex where the report has 1st and 2nd
        (
            "Lopadotemachoselachogaleokranioleipsanodrimhypotrimmatosilphiokarabome"
            + "litokatakechymenokichlepikossyphophattoperisteralektryonoptekephalliok"
            + "igklopeleiolagoiosiraiobaphetraganopterygon is a good dish."
        )
        # invalid example where the report has 1st through 3rd
    ]:
        print("\n" + text + "\n")
        print(validate(text).verbose)


if __name__ == "__main__":
    if len(argv) == 1:
        test()
    else:
        try:
            with open(argv[1], "rt") as infile:
                text = infile.read()
                print(validate(text).verbose)
        except FileNotFoundError as e:
            print(e)
