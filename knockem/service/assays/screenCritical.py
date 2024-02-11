from ...analysis import score_competition
from ...common import records as rec
from .. import orchestration as orch
from ._impl import add_competition, make_knockout_genome_id


def dispatch_depended_assays(assayDocument: dict) -> int:
    assayId = assayDocument["assayId"]
    submissionId = assayDocument["submissionId"]
    if orch.depends_on_unresolved(assayId):
        return 0  # dependencies already set up
    elif rec.does_submission_have_assay_result_of_type(
        submissionId=submissionId, assayType="nulldist"
    ):
        return 0  # have dependend on result
    elif depended := [
        *orch.iter_submission_assayIds_of_type(submissionId, "nulldist")
    ]:
        # add dependency to existing assay
        orch.add_dependency(
            dependedById=assayId,
            dependsOnId=depended[0],
            submissionId=submissionId,
            userEmail=assayDocument["userEmail"],
        )
        return 1
    else:
        # create new assay and depend on it
        nulldistAssayId = rec.add_assay(
            assayDesignation={},
            assayType="nulldist",
            competitionTimeoutSeconds=assayDocument[
                "competitionTimeoutSeconds"
            ],
            containerEnv=assayDocument["containerEnv"],
            containerImage=assayDocument["containerImage"],
            dependsOnIds=[],
            genomeIdAlpha=assayDocument["genomeIdAlpha"],
            maxCompetitionsActive=assayDocument["maxCompetitionsActive"],
            maxCompetitionRetries=assayDocument["maxCompetitionRetries"],
            submissionId=submissionId,
            userEmail=assayDocument["userEmail"],
        )
        orch.enqueue_assay(
            assayDesignation={},
            assayId=nulldistAssayId,
            assayType="nulldist",
            competitionTimeoutSeconds=assayDocument[
                "competitionTimeoutSeconds"
            ],
            containerEnv=assayDocument["containerEnv"],
            containerImage=assayDocument["containerImage"],
            dependedByIds=[assayId],
            dependsOnIds=[],
            genomeIdAlpha=assayDocument["genomeIdAlpha"],
            maxCompetitionsActive=assayDocument["maxCompetitionsActive"],
            maxCompetitionRetries=assayDocument["maxCompetitionRetries"],
            submissionId=submissionId,
            userEmail=assayDocument["userEmail"],
        )
        return 1


def dispatch_depended_competitions(assayDocument: dict) -> int:
    if orch.get_num_assay_competitions(assayDocument["assayId"]):
        return 0

    num_dispatched = 0
    genomeDocument = rec.get_genome_document(assayDocument["genomeIdAlpha"])
    for genomeSite in range(genomeDocument["genomeNumSites"]):
        knockoutSites = str(genomeSite)
        genomeIdBeta = make_knockout_genome_id(
            assayDocument=assayDocument,
            genomeDocument=genomeDocument,
            knockoutSites=knockoutSites,
        )
        add_competition(
            assayDocument=assayDocument,
            genomeIdAlpha=assayDocument["genomeIdAlpha"],
            genomeIdBeta=genomeIdBeta,
            knockoutSites=knockoutSites,
            competitionDesignation={"genomeSite": genomeSite},
        )
        num_dispatched += 1

    return num_dispatched


def finalize_result(assayDocument: dict) -> dict:
    assayId = assayDocument["assayId"]
    submissionId = assayDocument["submissionId"]
    competitionResults = rec.get_assay_competition_results(assayId)
    nulldistResult = rec.get_submission_assay_result_of_type(
        submissionId, "nulldist"
    )
    deleteriousThresh = nulldistResult["assayResult"]["sampledScoreQuantiles"][
        "99"
    ]
    beneficialThresh = nulldistResult["assayResult"]["sampledScoreQuantiles"][
        "1"
    ]
    siteScores = {
        rec.get_competition_document(res["competitionId"])[
            "competitionDesignation"
        ]["genomeSite"]: score_competition(
            resultNumAlpha=res["resultNumAlpha"],
            resultNumBeta=res["resultNumBeta"],
            resultUpdatesElapsed=res["resultNumUpdatesElapsed"],
        )
        for res in competitionResults
    }
    criticalSitesDeleterious = [
        site for site, score in siteScores.items() if score >= deleteriousThresh
    ]
    criticalSitesBeneficial = [
        site for site, score in siteScores.items() if score <= beneficialThresh
    ]
    criticalSitesCombined = sorted(
        {*criticalSitesDeleterious, *criticalSitesBeneficial},
    )
    numSitesTested = len(siteScores)
    falsePositiveCorrection = 0.01 * numSitesTested
    result = {
        "criticalSitesBeneficial": criticalSitesBeneficial,
        "criticalSitesCombined": criticalSitesCombined,
        "criticalSitesDeleterious": criticalSitesDeleterious,
        "estCriticalSitesBeneficial": len(criticalSitesBeneficial)
        - falsePositiveCorrection,
        "estCriticalSitesCombined": len(criticalSitesCombined)
        - falsePositiveCorrection * 2,
        "estCriticalSitesDeleterious": len(criticalSitesDeleterious)
        - falsePositiveCorrection,
        "numCriticalSitesBeneficial": len(criticalSitesBeneficial),
        "numCriticalSitesCombined": len(criticalSitesCombined),
        "numCriticalSitesDeleterious": len(criticalSitesDeleterious),
        "numTestedSites": len(siteScores),
    }
    rec.add_assay_result(
        assayId=assayDocument["assayId"],
        assayResult=result,
        submissionId=assayDocument["submissionId"],
        userEmail=assayDocument["userEmail"],
    )
    orch.complete_assay(assayDocument["assayId"])
    return result
