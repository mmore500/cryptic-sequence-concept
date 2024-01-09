import typing

import numpy as np


def skeletonize_naive(
    num_sites: int,
    test_knockout: typing.Callable,
) -> np.array:
    """Sample a knockout set where all remaining sites are detectably critical,
    i.e., cannot be removed without detectable fitness effects.

    Parameters
    ----------
    num_sites : int
        Number of sites in genome
    test_knockout : typing.Callable
        A function that tests the effect of a knockout, returning True if a
        knockout effect was detected and False otherwise.

        It should take boolean mask, e.g., produced by `sample_knockout`.

    Returns
    -------
    np.array
        A binary mask where 1 represents a knockout at a site and 0 represents
        no knockout.

        The length of the array is equal to `num_sites`.
    """
    knocked_out = np.zeros(num_sites, dtype=bool)

    while True:
        extended_knockout = _try_extend_knockout(test_knockout, knocked_out)
        assert extended_knockout.sum() >= knocked_out.sum()
        if np.array_equal(extended_knockout, knocked_out):
            break
        assert extended_knockout.sum() > knocked_out.sum() >= 0
        knocked_out = extended_knockout
        assert knocked_out.sum() > 0

    return knocked_out


def _try_extend_knockout(
    test_knockout: typing.Callable,
    base_knockout: np.array,
) -> np.array:
    """Implementation detail for `skeletonize_naive` that performs an exhaustive
    search for a site that can be knocked out without detectable fitness effects.

    Returns knockout mask with one additional site knocked out, or the original
    knockout mask if no additional sites can be knocked out without detectable
    fitness effects.
    """

    candidate_sites = np.flatnonzero(~base_knockout)
    np.random.shuffle(candidate_sites)
    assert candidate_sites.size == (~base_knockout).sum()
    for site in candidate_sites:
        knockout = base_knockout.copy()
        assert not knockout[site]
        knockout[site] = 1
        knockout_result = test_knockout(knockout)
        if knockout_result < 0:
            raise NotImplementedError(
                "Adaptive knockout result {knockout_result} ocurred for "
                f"site {site} with knockout {knockout}; naive skeletonization "
                "only accounts for deleterious or neutral knockout outcomes.",
            )
        if knockout_result == 0:
            return knockout
    else:
        return base_knockout
