import logging
import pprint

from .. import orchestration as orch
from ...common.records import get_submission_assay_results
from ..admin import email_submission_status


def submission_completion() -> int:
    num_completed = 0
    for submissionId in orch.iter_active_submissionIds():
        if orch.depends_on_unresolved(submissionId):
            continue

        document = orch.get_submission_document(submissionId)
        email_submission_status(
            submissionId,
            document["userEmail"],
            "completed",
            pprint.pformat(get_submission_assay_results(submissionId)),
        )
        orch.complete_submission(submissionId)

        num_completed += 1

    if num_completed > 0:
        logging.info(f"Completed {num_completed} submissions.")
    return num_completed
