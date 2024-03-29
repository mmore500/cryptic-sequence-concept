import logging
import subprocess
import uuid

from .. import orchestration as orch
from ...container import compete_two, get_env_from_document, pack_env_args


def _run_competition(document: dict) -> None:
    knockem_env = {
        "KNOCKEM_ASSAY_ID": document["assayId"],
        "KNOCKEM_COMPETITION_ID": document["competitionId"],
        "KNOCKEM_COMPETITION_ATTEMPT_ID": str(uuid.uuid4()),
        "KNOCKEM_CONTAINER_IMAGE": document["containerImage"],
        "KNOCKEM_GENOME_ID_ALPHA": document["genomeIdAlpha"],
        "KNOCKEM_GENOME_ID_BETA": document["genomeIdBeta"],
        "KNOCKEM_NUM_KNOCKOUT_SITES": len(document["knockoutSites"].split()),
        "KNOCKEM_RUNMODE": document["knockemRunmode"],
        "KNOCKEM_SUBMISSION_ID": document["submissionId"],
        "KNOCKEM_USER_EMAIL": document["userEmail"],
    }
    knockem_env = [
        elem
        for key, value in knockem_env.items()
        for elem in ["--env", f"{key}={value}"]
    ]
    command = (
        [
            "singularity",
            "run",
            # "--env",  # this should already be in env and get passed thru
            # 'KNOCKEM_RECORDS_URI="${KNOCKEM_RECORDS_URI}"',
        ]
        + knockem_env
        + document["containerEnv"].split()
        + document["containerEnv"]
        .replace("--env ", "--env KNOCKEM_FWD__")
        .split()
        + [
            f"docker://{document['containerImage']}",
            "knockem_compete_two",
        ]
    )
    logging.info(f"Running competition with command: {' '.join(command)}")
    subprocess.Popen(command)


def competition_kickoff() -> int:
    num_launched = 0
    for competitionId in orch.iter_pending_competitionIds():
        document = orch.get_competition_document(competitionId)
        if (
            orch.get_num_active_competitions(document["submissionId"])
            >= document["maxCompetitionsActive"]
        ):
            continue

        envArgs = " ".join(
            [
                pack_env_args(get_env_from_document(document)),
                document["containerEnv"],
            ]
        )
        compete_two(document["containerImage"], envArgs)

        orch.activate_competition(competitionId)
        num_launched += 1

    if num_launched > 0:
        logging.info(f"Launched {num_launched} competitions.")
    return num_launched
