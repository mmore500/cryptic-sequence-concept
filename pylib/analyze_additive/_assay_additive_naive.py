import typing

import numpy as np

from ._fit_negbinom_quantiles import fit_negbinom_quantiles
from ._sample_knockout import sample_knockout


def assay_additive_naive(
    test_knockout: typing.Callable,
    num_sites: int,
    knockout_doses: typing.List[int],
    num_replications: int = 100,
) -> dict:
    sensitivities = [
        np.mean(
            [
                test_knockout(sample_knockout(dose, num_sites))
                for __ in range(num_replications)
            ],
        )
        for dose in knockout_doses
    ]
    fit = fit_negbinom_quantiles(
        knockout_doses,
        sensitivities,
    )
    return {
        "num additive sites": fit["p"] * num_sites,
        "per-site effect size": 1 / fit["r"],
        "negative binomial fit": fit,
        "knockout doses": knockout_doses,
        "dose sensitivies": sensitivities,
    }
