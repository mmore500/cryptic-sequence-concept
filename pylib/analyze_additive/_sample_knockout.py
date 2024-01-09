import numpy as np


def sample_knockout(num_knockouts: int, num_sites: int) -> np.array:
    res = np.zeros(num_sites)
    res[np.random.choice(num_sites, num_knockouts, replace=False)] = 1
    return res
