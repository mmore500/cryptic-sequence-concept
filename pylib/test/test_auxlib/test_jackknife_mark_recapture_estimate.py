import pytest

from pylib.auxlib._jackknife_mark_recapture_estimate import (
    jackknife_mark_recapture_estimate,
    _Tk,
    _NJk,
    _NJk_v2,
)


# adapted from
# Burnham, Kenneth P., and W. Scott Overton.
# "Robust estimation of population size when capture probabilities vary among
# animals." Ecology 60.5 (1979): 927-936.
# https://doi.org/10.2307/1936861
# and data from
# Edwards, William R., and Lee Eberhardt. "Estimating cottontail abundance
# from livetrapping data." The Journal of Wildlife Management (1967): 87-96.
# https://doi.org/10.2307/3798362


def test_Njk():
    f = [43, 16, 8, 6, 0, 2, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    assert len(f) == 18

    assert abs(_NJk(0)(f) - 76) < 1
    assert abs(_NJk(1)(f) - 116.6) < 1
    assert abs(_NJk(2)(f) - 141.5) < 1
    assert abs(_NJk(3)(f) - 158.6) < 1
    assert abs(_NJk(4)(f) - 170.3) < 1
    assert abs(_NJk(5)(f) - 176.5) < 1


def test_Njk_v2():
    f = [43, 16, 8, 6, 0, 2, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    assert len(f) == 18

    assert pytest.approx(_NJk(0)(f)) == _NJk_v2(0)(f)
    assert pytest.approx(_NJk(1)(f)) == _NJk_v2(1)(f)
    assert pytest.approx(_NJk(2)(f)) == _NJk_v2(2)(f)
    assert pytest.approx(_NJk(3)(f)) == _NJk_v2(3)(f)
    assert pytest.approx(_NJk(4)(f)) == _NJk_v2(4)(f)
    assert pytest.approx(_NJk(5)(f)) == _NJk_v2(5)(f)


def test_Tk():
    f = [43, 16, 8, 6, 0, 2, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    assert len(f) == 18

    assert abs(_Tk(1)(f) - 4.053) < 0.1
    assert abs(_Tk(2)(f) - 2.071) < 0.1
    assert abs(_Tk(3)(f) - 1.071) < 0.1
    assert abs(_Tk(4)(f) - 0.417) < 0.1


def test_jackknife_mark_recapture_estimate():
    f = [43, 16, 8, 6, 0, 2, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    assert len(f) == 18

    assert abs(jackknife_mark_recapture_estimate(f) - 158.6) < 1
