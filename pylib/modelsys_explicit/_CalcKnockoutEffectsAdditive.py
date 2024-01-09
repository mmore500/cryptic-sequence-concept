import numpy as np


class CalcKnockoutEffectsAdditive:
    _additive_array: np.array

    def __init__(self, additive_array: np.array) -> None:
        self._additive_array = additive_array

    def __call__(self, knockout) -> float:
        active = self._additive_array * knockout
        return np.sum(active)
