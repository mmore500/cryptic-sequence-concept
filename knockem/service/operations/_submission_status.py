from connexion.exceptions import BadRequestProblem

from ...common.records import get_submission_assay_results
from ...common.records import has_submission as has_submission_records
from ..orchestration import (
    get_num_active_assays,
    get_num_active_competitions,
    get_num_completed_assays,
    get_num_completed_competitions,
    get_num_dependencies,
    get_num_failed_assays,
    get_num_failed_competitions,
    get_num_pending_assays,
    get_num_pending_competitions,
)
from ..orchestration import has_submission as has_submission_orchestration


def submission_status(submissionId: str) -> dict:
    if has_submission_orchestration(submissionId):
        return {
            "assayResults": get_submission_assay_results(submissionId),
            "numDependencies": get_num_dependencies(submissionId),
            "numActiveAssays": get_num_active_assays(submissionId),
            "numCompletedAssays": get_num_completed_assays(submissionId),
            "numFailedAssays": get_num_failed_assays(submissionId),
            "numPendingAssays": get_num_pending_assays(submissionId),
            "numActiveCompetitions": get_num_active_competitions(submissionId),
            "numCompletedCompetitions": get_num_completed_competitions(
                submissionId,
            ),
            "numFailedCompetitions": get_num_failed_competitions(submissionId),
            "numPendingCompetitions": get_num_pending_competitions(
                submissionId
            ),
            "submissionId": submissionId,
        }
    elif has_submission_records(submissionId):
        return {
            "assayResults": get_submission_assay_results(submissionId),
            "numDependencies": 0,
            "numActiveAssays": 0,
            "numCompletedAssays": float("nan"),
            "numFailedAssays": float("nan"),
            "numPendingAssays": 0,
            "numActiveCompetitions": 0,
            "numCompletedCompetitions": float("nan"),
            "numFailedCompetitions": float("nan"),
            "numPendingCompetitions": 0,
            "submissionId": submissionId,
        }
    else:
        raise BadRequestProblem(f"Submission {submissionId} does not exist.")
