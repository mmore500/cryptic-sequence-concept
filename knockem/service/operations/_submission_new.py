import uuid

from connexion.exceptions import BadRequestProblem

from ...common.records import (
    add_submission,
    add_genome,
    get_genome_document,
    is_genome_ephemeral,
)
from ..orchestration import enqueue_submission, has_user


def submission_new(
    body: dict,
) -> dict:
    return _submission_new(**body)


def _submission_new(
    containerEnv: dict,
    containerImage: str,
    competitionTimeoutSeconds: int,
    genomeContentAlpha: str,
    maxCompetitionsActive: int,
    maxCompetitionRetries: int,
    userEmail: str,
) -> dict:
    if not has_user(userEmail):
        raise BadRequestProblem(f"User {userEmail} is not registered.")

    containerEnv = " ".join(
        elem
        for key, value in containerEnv.items()
        for elem in ["--env", f"{key}='{value}'"]
    )

    submissionId = str(uuid.uuid4())
    genomeId = add_genome(
        genomeContent=genomeContentAlpha,
        isEphemeral=False,
        submissionId=submissionId,
        userEmail=userEmail,
    )
    assert not is_genome_ephemeral(genomeId)
    assert get_genome_document(genomeId) is not None
    submissionId = add_submission(
        competitionTimeoutSeconds=competitionTimeoutSeconds,
        containerEnv=containerEnv,
        containerImage=containerImage,
        hasAssayDoseCalibration=False,
        hasAssayDoseTitration=False,
        hasAssayNulldist=True,
        hasAssaySkeletonization=False,
        genomeIdAlpha=genomeId,
        maxCompetitionsActive=maxCompetitionsActive,
        maxCompetitionRetries=maxCompetitionRetries,
        submissionId=submissionId,
        userEmail=userEmail,
    )
    enqueue_submission(
        containerEnv=containerEnv,
        containerImage=containerImage,
        competitionTimeoutSeconds=competitionTimeoutSeconds,
        hasAssayDoseCalibration=False,
        hasAssayDoseTitration=False,
        hasAssayNulldist=True,
        hasAssaySkeletonization=False,
        genomeIdAlpha=genomeId,
        maxCompetitionsActive=maxCompetitionsActive,
        maxCompetitionRetries=maxCompetitionRetries,
        submissionId=submissionId,
        userEmail=userEmail,
    )

    return {"submissionId": submissionId}
