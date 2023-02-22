# Solutions for 2023-02-20 ("Adding it all up")

- [link](https://discourse.davidamos.dev/t/adding-it-all-up/139)

## TIO links

- [ArnoldC](https://tio.run/##lVRLj9owED4nv2K0Fy6t1JV66qlOmBBrbU9qO6AcaRetEGyoEOyhf56OAwGxOPs4el7fYyaZb9vN@vHP4SD9yIEraealxjTxQj2AJ/AlQinMGO5k@3e/gzm0@@ffi@2PuzQpsYG8tNJ5LRx4iwjLUJQmDdXg0EPtoK7gW7R0s9/Fayf84KAF4VygoIV1/eAxgfRgaJYmEmbC@FAg3ENoAAFZbfISqIBfNTovyTgI3C@lpZhi0KQ57mZokZNa41gKj6oZwO6ZnsFht13O26ee1I1Xp4bAqQPMEA14tFoaxhmnqWIjQogBEKZo2RxhsaiVak6zUwkGmV1HJlfEs93xkRH5o6zuqcmTzZtcIbTpRB7lOYQKqeKYkDbq/r/FdvPa@58SlGR6nQsnPXlJVYX2VF@yYyAd6AakmUovgsdhZ539nDPU@Qf9WwdWCRqqJyUEn9Ikw1zUTFCONExImkmAcqIBpitczyyRI6XYOMhE/tAjdGYaAouuwtxDQRYUTWQeldgunua75ctiUGak53m/fpmvX3fcRy25zB@0RXEXFQU4YiN45UKzJGM4@llXLmBRKhyOkwgZFjPiXCHDuX9lMdfQsYG9DwNTz@l3Rn9@advFLrKA@B9kFdlT7A42u8dNe3sGzKmylCnUlA6YOuhpKD8CXunlfw5fq7BU8@d5xo0N73UOQJzTJ6DVR5a2Ghy3ukz60Pov1Ievavi2b8jmpVQqfcuGt124urL@9q4Qrv4Wp7ZSOC9ACZjyNYgvnMuaw@H@@38)
- [APL](https://tio.run/##SyzI0U2pTMzJT///v6QoMzEv/VHbhGoNDQObR71bNXU1DOxAtObh6Rra@o96N9eAeLVcXI/6pgLVQTQoGBmg8g@tNzZFFTH4/x8A)

## Python benchmarks

| Function           |       14 |      -15 |      120 |        0 | `range(-3, 3)` | `range(0, 8)` | `range(-20, 20)` |
| :----------------- | -------: | -------: | -------: | -------: | -------------: | ------------: | ---------------: |
| `loop`             | 0.513 µs | 0.474 µs | 2.001 µs | 0.042 µs |       1.112 µs |      1.384 µs |        11.127 µs |
| `listcomp`         | 0.345 µs | 0.417 µs | 1.712 µs | 0.041 µs |       1.535 µs |      1.900 µs |        14.650 µs |
| `recursive`        | 0.676 µs | 0.783 µs | 5.651 µs | 0.035 µs |       1.017 µs |      1.895 µs |        21.835 µs |
| `cached_recursive` | 0.052 µs | 0.051 µs | 0.114 µs | 0.058 µs |       0.583 µs |      0.606 µs |         2.749 µs |
| `gauss_sum`        | 0.052 µs | 0.113 µs | 0.065 µs | 0.040 µs |       0.694 µs |      0.668 µs |         4.003 µs |

## Rust benchmarks

### Raw output from program

```
All functions correct.
n = 14:
  `_loop` with 1000000 loops: 0 ns
  `reduce` with 1000000 loops: 1.544 ns
  `recursive` with 1000000 loops: 0 ns
  `memoized_recursive` with 100000 loops: 721.17 ns
  `gauss_sum` with 1000000 loops: 0 ns
n = -15:
  `_loop` with 1000000 loops: 0 ns
  `reduce` with 1000000 loops: 3.127 ns
  `recursive` with 1000000 loops: 0 ns
  `memoized_recursive` with 1000000 loops: 553.2429999999999 ns
  `gauss_sum` with 1000000 loops: 0 ns
n = 120:
  `_loop` with 1000000 loops: 0 ns
  `reduce` with 1000000 loops: 1.252 ns
  `recursive` with 1000000 loops: 0 ns
  `memoized_recursive` with 10000 loops: 4.439100000000001 µs
  `gauss_sum` with 1000000 loops: 0 ns
n = 0:
  `_loop` with 1000000 loops: 0 ns
  `reduce` with 1000000 loops: 1.575 ns
  `recursive` with 1000000 loops: 0 ns
  `memoized_recursive` with 1000000 loops: 34.797000000000004 ns
  `gauss_sum` with 1000000 loops: 0 ns
 r = -3..3
  `_loop` with 100000 loops: 21.549999999999997 ns
  `reduce` with 1000000 loops: 20.656999999999996 ns
  `recursive` with 1000000 loops: 19.195 ns
  `memoized_recursive` with 100000 loops: 211.27999999999997 ns
  `gauss_sum` with 1000000 loops: 19.215 ns
 r = 0..8
  `_loop` with 1000000 loops: 15.265 ns
  `reduce` with 1000000 loops: 16.962999999999997 ns
  `recursive` with 1000000 loops: 14.859 ns
  `memoized_recursive` with 10000 loops: 391.99999999999994 ns
  `gauss_sum` with 1000000 loops: 14.779 ns
 r = -20..20
  `_loop` with 1000000 loops: 111.18999999999998 ns
  `reduce` with 1000000 loops: 133.72400000000002 ns
  `recursive` with 1000000 loops: 122.46000000000002 ns
  `memoized_recursive` with 10000 loops: 1.7426000000000001 µs
  `gauss_sum` with 1000000 loops: 133.50199999999998 ns
```

### Table

| Function             |       14 |      -15 |       120 |       0 |  `-3..3` |   `0..8` | `-20..20` |
| :------------------- | -------: | -------: | --------: | ------: | -------: | -------: | --------: |
| `_loop`              |     0 ns |     0 ns |      0 ns |    0 ns |  21.5 ns |  15.3 ns |  111.2 ns |
| `reduce`             |   1.5 ns |   3.1 ns |    1.3 ns |  1.6 ns |  20.7 ns |  17.0 ns |  133.7 ns |
| `recursive`          |     0 ns |     0 ns |      0 ns |    0 ns |  19.2 ns |  14.9 ns |  122.5 ns |
| `memoized_recursive` | 721.2 ns | 533.2 ns | 4439.1 ns | 34.8 ns | 211.8 ns | 392.9 ns | 1742.6 ns |
| `gauss_sum`          |     0 ns |     0 ns |      0 ns |    0 ns |  19.2 ns |  14.8 ns |  133.5 ns |

## C benchmarks

```
76205685, 76205685
n = 14: 51.777 ns
n = -15: 29.877 ns
n = 120: 122.664 ns
n = 0: 2.513 ns
range -3 to 3: 42.782 ns
range 0 to 8: 62.296 ns
range -20 to 20: 643.859 ns
```

## Improved `gauss_sum`

I replaced `gauss_sum` with a streamlined implementation by
[@ruud](https://discourse.davidamos.dev/t/adding-it-all-up/139/5):

### Python

Old:

```python
def gauss_sum(n: int) -> int:
    """Return 1 + 2 + ... + n if n > 0, 0 if n == 0, and -1 - 2 - ... + n if n < 0."""
    if not isinstance(n, int):
        raise TypeError(f"Arugment {n!r} is not an integer.")
    if n > 0:
        return n * (n + 1) // 2
    if n == 0:
        return 0
    else:
        return -gauss_sum(-n)
```

New:

```python
def gauss_sum(n: int) -> int:
    """Return 1 + 2 + ... + n if n > 0, 0 if n == 0, and -1 - 2 - ... + n if n < 0."""
    if not isinstance(n, int):
        raise TypeError(f"Arugment {n!r} is not an integer.")
    return n * (abs(n) + 1) // 2
```

Original Python benchmark table (copied from above):

| Function           |       14 |      -15 |      120 |        0 | `range(-3, 3)` | `range(0, 8)` | `range(-20, 20)` |
| :----------------- | -------: | -------: | -------: | -------: | -------------: | ------------: | ---------------: |
| `loop`             | 0.513 µs | 0.474 µs | 2.001 µs | 0.042 µs |       1.112 µs |      1.384 µs |        11.127 µs |
| `listcomp`         | 0.345 µs | 0.417 µs | 1.712 µs | 0.041 µs |       1.535 µs |      1.900 µs |        14.650 µs |
| `recursive`        | 0.676 µs | 0.783 µs | 5.651 µs | 0.035 µs |       1.017 µs |      1.895 µs |        21.835 µs |
| `cached_recursive` | 0.052 µs | 0.051 µs | 0.114 µs | 0.058 µs |       0.583 µs |      0.606 µs |         2.749 µs |
| `gauss_sum`        | 0.052 µs | 0.113 µs | 0.065 µs | 0.040 µs |       0.694 µs |      0.668 µs |         4.003 µs |

Revised Python benchmark table:

| Function           |       14 |      -15 |      120 |        0 | `range(-3, 3)` | `range(0, 8)` | `range(-20, 20)` |
| :----------------- | -------: | -------: | -------: | -------: | -------------: | ------------: | ---------------: |
| `loop`             | 0.531 µs | 0.481 µs | 2.138 µs | 0.042 µs |       1.116 µs |      1.376 µs |        11.242 µs |
| `listcomp`         | 0.346 µs | 0.419 µs | 1.695 µs | 0.041 µs |       1.518 µs |      1.911 µs |        14.737 µs |
| `recursive`        | 0.676 µs | 0.782 µs | 5.645 µs | 0.035 µs |       1.015 µs |      1.900 µs |        21.874 µs |
| `cached_recursive` | 0.051 µs | 0.051 µs | 0.114 µs | 0.058 µs |       0.584 µs |      0.605 µs |         2.746 µs |
| `gauss_sum`        | 0.057 µs | 0.066 µs | 0.068 µs | 0.060 µs |       0.597 µs |      0.734 µs |         3.095 µs |

### Rust

Old:

```rust
fn gauss_sum(n: i64) -> i64 {
    if n > 0 {
        n * (n + 1) / 2
    } else if n == 0 {
        0
    } else {
        -gauss_sum(-n)
    }
}
```

New:

```rust
fn gauss_sum(n: i64) -> i64 {
    n * (n.abs() + 1) / 2
}
```

Old benchmarks (copied from above):

| Function             |       14 |      -15 |       120 |       0 |  `-3..3` |   `0..8` | `-20..20` |
| :------------------- | -------: | -------: | --------: | ------: | -------: | -------: | --------: |
| `_loop`              |     0 ns |     0 ns |      0 ns |    0 ns |  21.5 ns |  15.3 ns |  111.2 ns |
| `reduce`             |   1.5 ns |   3.1 ns |    1.3 ns |  1.6 ns |  20.7 ns |  17.0 ns |  133.7 ns |
| `recursive`          |     0 ns |     0 ns |      0 ns |    0 ns |  19.2 ns |  14.9 ns |  122.5 ns |
| `memoized_recursive` | 721.2 ns | 533.2 ns | 4439.1 ns | 34.8 ns | 211.8 ns | 392.9 ns | 1742.6 ns |
| `gauss_sum`          |     0 ns |     0 ns |      0 ns |    0 ns |  19.2 ns |  14.8 ns |  133.5 ns |

New benchmarks:

| Function             |        14 |      -15 |       120 |       0 |  `-3..3` |   `0..8` | `-20..20` |
| :------------------- | --------: | -------: | --------: | ------: | -------: | -------: | --------: |
| `_loop`              |      0 ns |     0 ns |      0 ns |    0 ns |  22.0 ns |  20.8 ns |  126.6 ns |
| `reduce`             |    4.3 ns |   3.1 ns |    1.3 ns |  1.6 ns |  21.2 ns |  19.6 ns |  142.6 ns |
| `recursive`          |      0 ns |     0 ns |      0 ns |    0 ns |  19.3 ns |  17.5 ns |  122.8 ns |
| `memoized_recursive` | 1041.8 ns | 536.4 ns | 4450.4 ns | 35.2 ns | 212.3 ns | 415.1 ns | 1704.7 ns |
| `gauss_sum`          |      0 ns |     0 ns |      0 ns |    0 ns |  17.3 ns |  10.6 ns |   68.9 ns |
