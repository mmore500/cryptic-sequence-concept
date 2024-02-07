import uuid

from connexion.exceptions import BadRequestProblem

from ...common.records import get_submission_assay_results
from ..orchestration import (
    get_num_active_competitions,
    get_num_completed_competitions,
    get_num_failed_competitions,
    get_num_pending_competitions,
    has_submission,
)


def submission_status(submissionId: str) -> dict:
    if not has_submission(submissionId):
        raise BadRequestProblem(f"Submission {submissionId} does not exist.")

    return {
        "assayResults": get_submission_assay_results(submissionId),
        "numActiveCompetitions": get_num_active_competitions(submissionId),
        "numCompletedCompetitions": get_num_completed_competitions(
            submissionId,
        ),
        "numFailedCompetitions": get_num_failed_competitions(submissionId),
        "numPendingCompetitions": get_num_pending_competitions(submissionId),
        "submissionId": submissionId,
    }
