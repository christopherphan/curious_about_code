"""
Several Python solutions to David Amos's Weekly Coding Challenge:
    https://discourse.davidamos.dev/t/adding-it-all-up/139
"""

_cache: dict[int, int] = {}  # Could've use functools.cache decorator


def loop(n: int) -> int:
    """Return 1 + 2 + ... + n if n > 0, 0 if n == 0, and -1 - 2 - ... + n if n < 0."""
    if not isinstance(n, int):
        raise TypeError(f"Arugment {n!r} is not an integer.")
    if n > 0:
        ret_val = 0
        for k in range(1, n + 1):
            ret_val += k
        return ret_val
    elif n == 0:
        return 0
    else:
        return -loop(-n)


def listcomp(n: int) -> int:
    """Return 1 + 2 + ... + n if n > 0, 0 if n == 0, and -1 - 2 - ... + n if n < 0."""
    if not isinstance(n, int):
        raise TypeError(f"Arugment {n!r} is not an integer.")
    if n > 0:
        return sum([k for k in range(n + 1)])
    elif n == 0:
        return 0
    else:
        return -listcomp(-n)


def recursive(n: int) -> int:
    """Return 1 + 2 + ... + n if n > 0, 0 if n == 0, and -1 - 2 - ... + n if n < 0."""
    if not isinstance(n, int):
        raise TypeError(f"Arugment {n!r} is not an integer.")
    if n == 0:
        return 0
    elif n > 0:
        return n + recursive(n - 1)
    else:
        return -recursive(-n)


def cached_recursive(n: int) -> int:
    """Return 1 + 2 + ... + n if n > 0, 0 if n == 0, and -1 - 2 - ... + n if n < 0."""
    if not isinstance(n, int):
        raise TypeError(f"Arugment {n!r} is not an integer.")
    if n not in _cache:
        if n == 0:
            _cache[n] = 0
        elif n > 0:
            _cache[n] = n + recursive(n - 1)
        else:
            _cache[n] = -recursive(-n)
    return _cache[n]


def gauss_sum(n: int) -> int:
    """Return 1 + 2 + ... + n if n > 0, 0 if n == 0, and -1 - 2 - ... + n if n < 0."""
    if not isinstance(n, int):
        raise TypeError(f"Arugment {n!r} is not an integer.")
    return n * (abs(n) + 1) // 2
