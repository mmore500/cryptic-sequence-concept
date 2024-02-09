import logging

from .. import orchestration as orch


def assay_completion() -> int:
    num_completed = 0
    for assayId in orch.iter_active_assayIds():
        if orch.depends_on_unresolved(assayId):
            continue

        orch.complete_assay(assayId)
        num_completed += 1

    if num_completed > 0:
        logging.info(f"Completed {num_completed} assays.")
    return num_completed
