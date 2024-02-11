import logging

from .. import orchestration as orch
from ...common import records as rec
from ...container import warm_image_cache


def _do_add_assay(assayType: str, submissionDocument: dict) -> None:
    document = submissionDocument
    assayId = rec.add_assay(
        assayDesignation={},
        assayType=assayType,
        competitionTimeoutSeconds=document["competitionTimeoutSeconds"],
        containerEnv=document["containerEnv"],
        containerImage=document["containerImage"],
        dependsOnIds=[],
        genomeIdAlpha=document["genomeIdAlpha"],
        maxCompetitionsActive=document["maxCompetitionsActive"],
        maxCompetitionRetries=document["maxCompetitionRetries"],
        submissionId=document["submissionId"],
        userEmail=document["userEmail"],
    )
    orch.enqueue_assay(
        assayDesignation={},
        assayId=assayId,
        assayType=assayType,
        competitionTimeoutSeconds=document["competitionTimeoutSeconds"],
        containerEnv=document["containerEnv"],
        containerImage=document["containerImage"],
        dependedByIds=[],
        dependsOnIds=[],
        genomeIdAlpha=document["genomeIdAlpha"],
        maxCompetitionsActive=document["maxCompetitionsActive"],
        maxCompetitionRetries=document["maxCompetitionRetries"],
        submissionId=document["submissionId"],
        userEmail=document["userEmail"],
    )


def submission_kickoff() -> int:
    num_launched = 0
    for submissionId in orch.iter_pending_submissionIds():
        document = orch.get_submission_document(submissionId)
        warm_image_cache(document["containerImage"])
        orch.activate_submission(submissionId)
        num_launched += 1

        if document["hasAssayNulldist"]:
            _do_add_assay("nulldist", document)

        if document["hasAssayScreenCritical"]:
            _do_add_assay("screenCritical", document)

    if num_launched > 0:
        logging.info(f"Launched {num_launched} submissions.")
    return num_launched
