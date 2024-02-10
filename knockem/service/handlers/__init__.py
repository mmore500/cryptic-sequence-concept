import logging

from ._assay_update import assay_update
from ._competition_completion import competition_completion
from ._competition_kickoff import competition_kickoff
from ._competition_timeout import competition_timeout
from ._submission_completion import submission_completion
from ._submission_fail import submission_fail
from ._submission_kickoff import submission_kickoff

__all__ = [
    "assay_update",
    "competition_completion",
    "competition_kickoff",
    "competition_timeout",
    "submission_completion",
    "submission_fail",
    "submission_kickoff",
]


def run_handlers() -> int:
    logging.info("Running handlers.")
    return sum(
        (
            assay_update(),
            competition_completion(),
            competition_kickoff(),
            competition_timeout(),
            submission_completion(),
            submission_fail(),
            submission_kickoff(),
        )
    )
