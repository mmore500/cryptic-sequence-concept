import numpy as np


def sample_knockout(dose: int, num_sites: int) -> np.array:
    res = np.zeros(num_sites)
    res[np.random.choice(num_sites, dose, replace=False)] = 1
    return res
