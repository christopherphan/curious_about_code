import sums


def test_sums():
    """Test all the sums functions."""
    for k in [15, -13, 7, 8, -30, 0]:
        assert sums.loop(k) == sums.listcomp(k)
        assert sums.loop(k) == sums.recursive(k)
        assert sums.loop(k) == sums.cached_recursive(k)
        assert sums.loop(k) == sums.gauss_sum(k)
