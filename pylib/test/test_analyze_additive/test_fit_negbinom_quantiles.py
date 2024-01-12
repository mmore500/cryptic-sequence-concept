import numpy as np
from scipy.stats import nbinom as scipy_negative_binomial

from pylib.analyze_additive import fit_negbinom_quantiles


def test_fit_negbinom_quantiles_exact():
    n, p = 10, 0.44
    cumulative_probabilities = np.array([0.14, 0.34, 0.63, 0.8])
    counts = scipy_negative_binomial.ppf(cumulative_probabilities, n, p)
    result = fit_negbinom_quantiles(counts, cumulative_probabilities)
    assert isinstance(result, dict)
    assert "r" in result and "p" in result
    assert 0.35 < result["p"] < 0.45
    assert 8 < result["r"] < 12, result["fit quantiles"]
    assert len(result["fit quantiles"]) == 4


def test_fit_negbinom_quantiles_noised():
    n, p = 3, 0.05
    quantiles = np.array([0.4, 0.5, 0.8])
    counts = scipy_negative_binomial.ppf(quantiles, n, p)
    noise = np.array([0.01, -0.02, 0.0])
    result = fit_negbinom_quantiles(counts, quantiles + noise)
    assert isinstance(result, dict)
    assert "r" in result and "p" in result
    assert 2 < result["r"] < 5
    assert 0.01 < result["p"] < 0.1
    assert len(result["fit quantiles"]) == 3
