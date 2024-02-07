import logging

from .. import orchestration as orch
from .. import records as rec


def competition_completion() -> int:
    num_completed = 0
    for competitionId in orch.iter_active_competitionIds():
        if not rec.has_competition_result(competitionId):
            continue

        orch.complete_competition(competitionId)
        num_completed += 1

    if num_completed > 0:
        logging.info(f"Completed {num_completed} competitions.")
    return num_completed
