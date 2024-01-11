import typing
import warnings

from iterpop import iterpop as ip
import numpy as np

from ..auxlib._jackknife_mark_recapture_estimate import (
    jackknife_mark_recapture_estimate,
)


def assay_agnostic_naive(
    skeletons_description_df: typing.Sequence[np.array],
) -> dict:
    num_skeletons = ip.pophomogeneous(
        skeletons_description_df["skeleton outcome count, included"]
        + skeletons_description_df["skeleton outcome count, excluded"]
    )
    if num_skeletons < 5:
        warnings.warn(
            "Burnham and Overton recommend at least five capture/recapture "
            f"observations, but only {num_skeletons} provided.",
        )

    f = np.bincount(
        skeletons_description_df["skeleton outcome count, included"].astype(
            int
        ),
    )[1:].copy()
    f.resize(num_skeletons)
    estimate, ci = jackknife_mark_recapture_estimate(f)

    return {
        "num sites estimate": estimate,
        "num sites 95% CI": ci,
    }
