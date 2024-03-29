import threading
import uuid

from ...common.records import (
    add_genome,
    add_submission,
    get_genome_document,
    is_genome_ephemeral,
)
from ...container import pack_env_args
from ..admin import email_submission_status
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

    def do_submission_new():
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
        add_submission(
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
        email_submission_status(
            submissionId, userEmail, "pending", genomeContentAlpha
        )

    # this operation might require a SIF build, so put in a background thread
    # so that the API request can return
    background_thread = threading.Thread(target=do_submission_new)
    background_thread.start()

    return {"submissionId": submissionId}
