import logging

from .. import orchestration as orch


def submission_completion() -> int:
    num_completed = 0
    for submissionId in orch.iter_active_submissionIds():
        if orch.depends_on_unresolved(submissionId):
            continue

        orch.complete_submission(submissionId)
        num_completed += 1

    if num_completed > 0:
        logging.info(f"Completed {num_completed} submissions.")
    return num_completed
