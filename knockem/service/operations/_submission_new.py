import uuid

from connexion.exceptions import BadRequestProblem

from ..orchestration import add_submission as add_submission_orchestration
from ..orchestration import has_user, enqueue_assay
from ...common.records import add_genome, add_assay
from ...common.records import add_submission as add_submission_record


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
        submissionId=submissionId,
        userEmail=userEmail,
    )
    submissionId = add_submission_record(
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
    add_submission_orchestration(
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

    assayId = add_assay(
        assayType="nulldist",
        competitionTimeoutSeconds=competitionTimeoutSeconds,
        containerEnv=containerEnv,
        containerImage=containerImage,
        dependsOnIds=[],
        genomeIdAlpha=genomeId,
        maxCompetitionsActive=maxCompetitionsActive,
        maxCompetitionRetries=maxCompetitionRetries,
        submissionId=submissionId,
        userEmail=userEmail,
    )
    enqueue_assay(
        assayId=assayId,
        assayType="nulldist",
        competitionTimeoutSeconds=competitionTimeoutSeconds,
        containerEnv=containerEnv,
        containerImage=containerImage,
        dependsOnIds=[],
        genomeIdAlpha=genomeId,
        maxCompetitionsActive=maxCompetitionsActive,
        maxCompetitionRetries=maxCompetitionRetries,
        submissionId=submissionId,
        userEmail=userEmail,
    )

    return {"submissionId": submissionId}
