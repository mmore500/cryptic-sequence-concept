import numpy as np

from pylib.analyze_epistasis import skeletonize_naive


def test_skeletonize_naive_knockout_all_sites_sensitive():
    def mock_test_knockout(knockout: np.array) -> bool:
        return np.any(knockout)  # sensitive to any knockout

    num_sites = 10
    result = skeletonize_naive(num_sites, mock_test_knockout)

    assert len(result) == num_sites  # correct length
    assert not np.any(result)  # no sites should be knocked out


def test_skeletonize_naive_knockout_effect_no_sites_sensitive():
    def mock_test_knockout(knockout: np.array) -> bool:
        return False  # sensitive to no knockouts

    num_sites = 10
    knockout_result = skeletonize_naive(num_sites, mock_test_knockout)

    assert len(knockout_result) == num_sites  # correct length
    assert np.all(knockout_result)  # all sites should be knocked out


def test_skeletonize_naive_single_sensitive_site():
    def mock_test_knockout(knockout):
        return knockout[0]  # sensitive to only the first site

    expected = np.array([0, 1, 1])
    result = skeletonize_naive(expected.size, mock_test_knockout)
    assert np.array_equal(result, expected)
