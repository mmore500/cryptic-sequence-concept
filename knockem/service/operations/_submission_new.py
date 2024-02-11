import uuid

from connexion.exceptions import BadRequestProblem

from ...common.records import (
    add_genome,
    add_submission,
    get_genome_document,
    is_genome_ephemeral,
)
from ...container import pack_env_args
from ..orchestration import enqueue_submission


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

    packedContainerEnv = pack_env_args(containerEnv)

    submissionId = str(uuid.uuid4())
    genomeId = add_genome(
        containerEnv=packedContainerEnv,
        containerImage=containerImage,
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
        hasAssayNulldist=False,
        hasAssayScreenCritical=True,
        hasAssaySkeletonization=False,
        genomeIdAlpha=genomeId,
        maxCompetitionsActive=maxCompetitionsActive,
        maxCompetitionRetries=maxCompetitionRetries,
        submissionId=submissionId,
        userEmail=userEmail,
    )
    enqueue_submission(
        containerEnv=packedContainerEnv,
        containerImage=containerImage,
        competitionTimeoutSeconds=competitionTimeoutSeconds,
        hasAssayDoseCalibration=False,
        hasAssayDoseTitration=False,
        hasAssayNulldist=False,
        hasAssayScreenCritical=True,
        hasAssaySkeletonization=False,
        genomeIdAlpha=genomeId,
        maxCompetitionsActive=maxCompetitionsActive,
        maxCompetitionRetries=maxCompetitionRetries,
        submissionId=submissionId,
        userEmail=userEmail,
    )

    return {"submissionId": submissionId}
