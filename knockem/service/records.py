from pymongo import MongoClient

from .meta import with_common_columns


def get_db():
    return MongoClient().knockem


# genomes =====================================================================
def add_genome(genomeContent: str, submissionId: str, userEmail: str) -> str:
    row = with_common_columns(
        "_id",
        genomeContent=genomeContent,
        submissionId=submissionId,
        userEmail=userEmail,
    )
    row["genomeId"] = row["_id"]
    get_db().genomes.insert_one(row)
    return row["_id"]


def delete_genome_document(genomeId: str) -> None:
    get_db().genomes.delete_one({"_id": genomeId})


def get_genome_document(genomeId: str) -> dict:
    return get_db().genomes.find_one({"_id": genomeId})


def is_genome_ephemeral(genomeId: str) -> bool:
    return bool(
        get_db().competitionResults.count_documents(
            {"_id": genomeId, "isEphemeral": True},
            limit=1,
        ),
    )


# submissions =================================================================
def add_submission(
    competitionTimeoutSeconds: int,
    containerEnv: str,
    containerImage: str,
    genomeIdAlpha: str,
    hasAssayDoseCalibration: bool,
    hasAssayDoseTitration: bool,
    hasAssayNulldist: bool,
    hasAssaySkeletonization: bool,
    maxCompetitionsActive: int,
    maxCompetitionsFail: int,
    userEmail: str,
) -> str:
    row = with_common_columns(
        "submissionId",
        "_id",
        competitionTimeoutSeconds=competitionTimeoutSeconds,
        containerEnv=containerEnv,
        containerImage=containerImage,
        genomeIdAlpha=genomeIdAlpha,
        hasAssayDoseCalibration=hasAssayDoseCalibration,
        hasAssayDoseTitration=hasAssayDoseTitration,
        hasAssayNulldist=hasAssayNulldist,
        hasAssaySkeletonization=hasAssaySkeletonization,
        maxCompetitionsActive=maxCompetitionsActive,
        maxCompetitionsFail=maxCompetitionsFail,
        status="active",
        userEmail=userEmail,
    )
    get_db().submissions.insert_one(row)
    return row["_id"]


# assays ======================================================================
def add_assay(
    assayType: str,
    competitionTimeoutSeconds: int,
    containerEnv: str,
    containerImage: str,
    dependsOnIds: list[str],
    genomeIdAlpha: str,
    maxCompetitionsActive: int,
    maxCompetitionsFail: int,
    submissionId: str,
    userEmail: str,
) -> str:
    row = with_common_columns(
        "assayId",
        "_id",
        assayType=assayType,
        competitionTimeoutSeconds=competitionTimeoutSeconds,
        containerEnv=containerEnv,
        containerImage=containerImage,
        dependsOnIds=dependsOnIds,
        genomeIdAlpha=genomeIdAlpha,
        maxCompetitionsActive=maxCompetitionsActive,
        maxCompetitionsFail=maxCompetitionsFail,
        submissionId=submissionId,
        userEmail=userEmail,
    )
    get_db().assays.insert_one(row)
    return row["_id"]


def add_assay_result(
    assayId: str,
    assayResult: dict,
    submissionId: str,
    userEmail: str,
) -> None:
    row = with_common_columns(
        assayId=assayId,
        assayResult=assayResult,
        submissionId=submissionId,
        userEmail=userEmail,
        _id=assayId,
    )
    get_db().assayResults.insert_one(row)


def has_assay_result(assayId: str) -> bool:
    return bool(
        get_db().assayResults.count_documents(
            {"_id": assayId},
            limit=1,
        ),
    )


# competitios =================================================================
def add_competition(
    assayId: str,
    genomeIdAlpha: str,
    genomeIdBeta: str,
    knockoutSites: str,
    submissionId: str,
    userEmail: str,
) -> str:
    row = with_common_columns(
        "competitionId",
        "_id",
        assayId=assayId,
        genomeIdAlpha=genomeIdAlpha,
        genomeIdBeta=genomeIdBeta,
        knockoutSites=knockoutSites,
        numKnockoutSites=len(knockoutSites.split()),
        submissionId=submissionId,
        userEmail=userEmail,
    )
    get_db().assays.insert_one(row)
    return row["_id"]


def add_competition_result(
    assayId: str,
    competitionId: str,
    knockoutSites: str,
    resultUpdatesElapsed: int,
    resultNumAlpha: int,
    resultNumBeta: int,
    submissionId: str,
    userEmail: str,
) -> bool:
    if has_competition_result(competitionId):
        return False
    else:
        row = with_common_columns(
            assayId=assayId,
            competitionId=competitionId,
            knockoutSites=knockoutSites,
            numKnockoutSites=len(knockoutSites.split()),
            resultUpdatesElapsed=resultUpdatesElapsed,
            resultNumAlpha=resultNumAlpha,
            resultNumBeta=resultNumBeta,
            submissionId=submissionId,
            userEmail=userEmail,
            _id=competitionId,
        )
        get_db().assayResults.insert_one(row)
        return True


def has_competition_result(competitionId: str) -> bool:
    return bool(
        get_db().competitionResults.count_documents(
            {"_id": competitionId},
            limit=1,
        ),
    )


# cleanup =====================================================================
def purge_submission(submissionId: str):
    for collection in get_db():
        collection.delete_many({"submissionId": submissionId})


def purge_testing():
    for collection in get_db():
        collection.delete_many({"knockemRunmode": "testing"})
