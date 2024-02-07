import logging
import subprocess
import uuid

from .. import orchestration as orch
from .. import records as rec


def _run_competition(document: dict) -> None:
    knockem_env = {
        "KNOCKEM_ASSAY_ID": document["assayId"],
        "KNOCKEM_COMPETITION_ID": document["competitionId"],
        "KNOCKEM_COMPETITION_ATTEMPT_ID": str(uuid.uuid4()),
        "KNOCKEM_RECORDS_URI": rec.get_records_uri(),
        "KNOCKEM_GENOME_ID_ALPHA": document["genomeIdAlpha"],
        "KNOCKEM_GENOME_ID_BETA": document["genomeIdBeta"],
        "KNOCKEM_RUNMODE": document["knockemRunmode"],
        "KNOCKEM_SUBMISSION_ID": document["submissionId"],
        "KNOCKEM_USER_EMAIL": document["userEmail"],
    }
    knockem_env = [
        elem
        for key, value in knockem_env.items()
        for elem in ["--env", f"{key}='{value}'"]
    ]
    subprocess.Popen(
        [
            "singularity",
            "run",
            document["containerImage"],
            "knockem_compete_two",
            "--env",
            'KNOCKEM_RECORDS_CREDENTIAL="${KNOCKEM_RECORDS_CREDENTIAL}"',
        ]
        + knockem_env
        + document["containerEnv"].split(),
    )


def competition_kickoff() -> int:
    num_launched = 0
    for competitionId in orch.iter_pending_competitionIds():
        document = orch.get_competition_document(competitionId)
        if (
            orch.get_num_active_competitions()
            >= document["maxCompetitionsActive"]
        ):
            continue

        _run_competition(document)

        orch.activate_competition(competitionId)
        num_launched += 1

    if num_launched > 0:
        logging.info(f"Launched {num_launched} competitions.")
    return num_launched
