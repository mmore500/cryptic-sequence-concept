import logging

from .. import orchestration as orch
from ...common import records as rec


def assay_kickoff() -> int:
    num_launched = 0
    for assayId in orch.iter_pending_assayIds():
        if orch.depends_on_unresolved(assayId):
            continue

        document = orch.get_assay_document(assayId)
        if document["assayType"] == "nulldist":
            competitions = [
                (document["genomeIdAlpha"], document["genomeIdAlpha"], "")
                for __ in range(100)
            ]
        else:
            raise NotImplementedError(
                f"Assay type {document['assayType']} is not supported.",
            )

        competitionIds = [
            rec.add_competition(
                assayId=assayId,
                genomeIdAlpha=alpha,
                genomeIdBeta=beta,
                knockoutSites=ko,
                submissionId=document["submissionId"],
                userEmail=document["userEmail"],
            )
            for alpha, beta, ko in competitions
        ]
        for competitionId, (alpha, beta, ko) in zip(
            competitionIds, competitions
        ):
            orch.enqueue_competition(
                assayId=assayId,
                competitionId=competitionId,
                competitionTimeoutSeconds=document["competitionTimeoutSeconds"],
                containerEnv=document["containerEnv"],
                containerImage=document["containerImage"],
                genomeIdAlpha=alpha,
                genomeIdBeta=beta,
                knockoutSites=ko,
                maxCompetitionsActive=document["maxCompetitionsActive"],
                maxCompetitionRetries=document["maxCompetitionRetries"],
                submissionId=document["submissionId"],
                userEmail=document["userEmail"],
            )

        num_launched += 1

    if num_launched > 0:
        logging.info(f"Launched {num_launched} assays.")
    return num_launched
