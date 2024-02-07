import logging

from ._assay_completion import assay_completion
from ._assay_kickoff import assay_kickoff
from ._competition_completion import competition_completion
from ._competition_kickoff import competition_kickoff
from ._competition_timeout import competition_timeout
from ._submission_completion import submission_completion
from ._submission_fail import submission_fail

__all__ = [
    "assay_completion",
    "assay_kickoff",
    "competition_completion",
    "competition_kickoff",
    "competition_timeout",
    "submission_completion",
    "submission_fail",
]


def run_handlers() -> int:
    logging.info("Running handlers.")
    return sum(
        (
            assay_completion(),
            assay_kickoff(),
            competition_completion(),
            competition_kickoff(),
            competition_timeout(),
            submission_completion(),
            submission_fail(),
        )
    )


del logging  # prevent name leakage
