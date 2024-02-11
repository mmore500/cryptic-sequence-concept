import logging

from .. import orchestration as orch
from ...common import records as rec
from ...container import warm_image_cache


def submission_kickoff() -> int:
    num_launched = 0
    for submissionId in orch.iter_pending_submissionIds():
        document = orch.get_submission_document(submissionId)
        warm_image_cache(document["containerImage"])
        orch.activate_submission(submissionId)
        num_launched += 1

        if document["hasAssayNulldist"]:
            assayId = rec.add_assay(
                assayDesignation={},
                assayType="nulldist",
                competitionTimeoutSeconds=document["competitionTimeoutSeconds"],
                containerEnv=document["containerEnv"],
                containerImage=document["containerImage"],
                dependsOnIds=[],
                genomeIdAlpha=document["genomeIdAlpha"],
                maxCompetitionsActive=document["maxCompetitionsActive"],
                maxCompetitionRetries=document["maxCompetitionRetries"],
                submissionId=submissionId,
                userEmail=document["userEmail"],
            )
            orch.enqueue_assay(
                assayDesignation={},
                assayId=assayId,
                assayType="nulldist",
                competitionTimeoutSeconds=document["competitionTimeoutSeconds"],
                containerEnv=document["containerEnv"],
                containerImage=document["containerImage"],
                dependsOnIds=[],
                genomeIdAlpha=document["genomeIdAlpha"],
                maxCompetitionsActive=document["maxCompetitionsActive"],
                maxCompetitionRetries=document["maxCompetitionRetries"],
                submissionId=submissionId,
                userEmail=document["userEmail"],
            )

    if num_launched > 0:
        logging.info(f"Launched {num_launched} submissions.")
    return num_launched
