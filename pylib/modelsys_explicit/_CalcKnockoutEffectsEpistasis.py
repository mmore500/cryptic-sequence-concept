import typing

import numpy as np
import opytional as opyt
from scipy import stats as scipy_stats

from ..auxlib._nonzero import nonzero


class CalcKnockoutEffectsEpistasis:
    """Functor to model the contribution of epistatic interactions between
    genome sites to knockout outcomes."""

    _effect_thresh: int
    _effect_size: float
    _epistasis_matrix: np.array

    def __init__(
        self: "CalcKnockoutEffectsEpistasis",
        epistasis_matrix: np.array,
        effect_thresh: typing.Optional[int],
        effect_size: float = 1.0,
    ) -> None:
        """Initialize functor with epistatic interaction information.

        Parameters
        ----------
        epistasis_matrix : np.array
            Arrangement of epistatic set labels, where columns correspond to
            genome sites and rows allow each site to contain more than one
            epistatic value. Only nonzero values are considered as set labels.

            Can be generated via `create_epistasis_matrix_overlapping` or
            `create_epistasis_matrix_disjoint`.

        effect_thresh : int, optional
            The threshold number of activations required to consider an effect.
            If None, uses the largest set size in the epistatic matrix.

        effect_size : float, default=1.0
            The size of fitness effect when threshold sites within an epistatic
            set are knocked out.
        """
        self._effect_thresh = opyt.or_value(
            effect_thresh,
            scipy_stats.mode(nonzero(epistasis_matrix), axis=None).count,
        )
        self._effect_size = effect_size
        self._epistasis_matrix = epistasis_matrix

    def __call__(
        self: "CalcKnockoutEffectsEpistasis",
        knockout: np.array,
    ) -> float:
        """Calculate the fitness effect of a knockout considering epistatic
        interactions.

        Parameters
        ----------
        knockout : np.array
            A binary array representing knockout sites, where 1 indicates site
            knockout. Length of array corresponds to genome size.

        Returns
        -------
        float
            The fitness effect of knockouts from epistatic interactions.

            If the number of knocked out sites within an epistatic set exceeds
            `effect_thresh`, returns `effect_size`; otherwise, returns 0.0.
        """
        active_sites = self._epistasis_matrix * knockout
        max_set_activations = scipy_stats.mode(
            nonzero(active_sites), axis=None
        ).count

        return (max_set_activations >= self._effect_thresh) * self._effect_size
