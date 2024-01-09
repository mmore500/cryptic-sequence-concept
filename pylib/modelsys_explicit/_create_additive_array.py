import typing

import numpy as np


def create_additive_array(num_sites, rate, distn):
    res = np.zeros(num_sites)
    return _add_additive_effects(res, rate, distn)


def _add_additive_effects(
    array: np.array,
    rate,
    distn: typing.Callable = np.random.rand,
) -> np.array:
    num_sites = array.size
    num_effects = int(num_sites * rate)

    effects = distn(num_effects)
    indices = np.random.choice(num_sites, num_effects, replace=False)
    array[indices] += effects
    return array
