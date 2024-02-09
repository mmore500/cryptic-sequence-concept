import logging

from .. import orchestration as orch


def competition_timeout() -> int:
    num_requeued = 0
    for competitionId in orch.iter_active_competitionIds():
        document = orch.get_competition_document(competitionId)

        cur_time = orch._get_time()
        if (
            cur_time - document["activationTimestamp"]
            < document["competitionTimeoutSeconds"]
        ):
            continue

        try_count = document["competitionRetryCount"]
        if try_count >= document["maxCompetitionRetries"]:
            orch.fail_competition(competitionId)
            continue

        orch.requeue_competition(competitionId, retry=try_count + 1)
        num_requeued += 1

    if num_requeued > 0:
        logging.info(f"Requeued {num_requeued} competitions.")
    return num_requeued
