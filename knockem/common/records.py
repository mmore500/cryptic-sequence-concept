import json

import os
import requests

from .meta import with_common_columns


# import logging
# import functools
# from pymongo import MongoClient

# @functools.lru_cache
# def get_db():
#     env_key = "KNOCKEM_RECORDS_URI"
#     if env_key not in os.environ:
#         raise ValueError(f"Environment variable {env_key} is not set.")

#     uri = os.environ["KNOCKEM_RECORDS_URI"]
#     logging.info(f"Connecting to {uri}")
#     return MongoClient(uri).knockem


# Helper function for MongoDB Data API requests
def mongodb_data_api_request(
    action, collection, document=None, filter=None, update=None, projection=None
):
    url = f"https://us-east-2.aws.data.mongodb-api.com/app/data-tlhxq/endpoint/data/v1/action/{action}"
    api_key = os.getenv("KNOCKEM_MONGODB_DATA_API_KEY")
    if not api_key:
        raise ValueError(
            "KNOCKEM_MONGODB_DATA_API_KEY environment variable is not set.",
        )

    headers = {
        "Content-Type": "application/json",
        "Access-Control-Request-Headers": "*",
        "api-key": api_key,
    }

    payload = {
        "collection": collection,
        "database": "knockem",
        "dataSource": "knockem",  # Replace with your actual dataSource
    }
    if document is not None:
        payload["document"] = document
    if filter is not None:
        payload["filter"] = filter
    if update is not None:
        payload["update"] = update
    if projection is not None:
        payload["projection"] = projection

    response = requests.post(url, headers=headers, data=json.dumps(payload))
    if response.status_code < 400:
        return response.json()
    else:
        raise Exception(
            f"MongoDB Data API request failed with status code {response.status_code}: {response.text}",
        )


# genomes =====================================================================
def add_genome(
    genomeContent: str, isEphemeral: bool, submissionId: str, userEmail: str
) -> str:
    row = with_common_columns(
        "genomeId",
        "_id",
        genomeContent=genomeContent,
        isEphemeral=isEphemeral,
        submissionId=submissionId,
        userEmail=userEmail,
    )
    # get_db().genomes.insert_one(row)
    mongodb_data_api_request("insertOne", "genomes", document=row)
    return row["genomeId"]


def delete_genome_document(genomeId: str) -> None:
    # get_db().genomes.delete_one({"genomeId": genomeId})
    mongodb_data_api_request(
        "deleteOne", "genomes", filter={"genomeId": genomeId}
    )


def get_genome_document(genomeId: str) -> dict:
    # return get_db().genomes.find_one({"genomeId": genomeId})
    result = mongodb_data_api_request(
        "findOne", "genomes", filter={"genomeId": genomeId}
    )
    return result.get("document")


def is_genome_ephemeral(genomeId: str) -> bool:
    # return bool(
    #     get_db().competitionResults.count_documents(
    #         {"genomeId": genomeId, "isEphemeral": True},
    #         limit=1,
    #     ),
    # )
    result = mongodb_data_api_request(
        "findOne",
        "competitionResults",
        filter={"genomeId": genomeId, "isEphemeral": True},
    )
    return result.get("document", None) is not None


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
    maxCompetitionRetries: int,
    submissionId: str,
    userEmail: str,
) -> str:
    row = with_common_columns(
        competitionTimeoutSeconds=competitionTimeoutSeconds,
        containerEnv=containerEnv,
        containerImage=containerImage,
        genomeIdAlpha=genomeIdAlpha,
        hasAssayDoseCalibration=hasAssayDoseCalibration,
        hasAssayDoseTitration=hasAssayDoseTitration,
        hasAssayNulldist=hasAssayNulldist,
        hasAssaySkeletonization=hasAssaySkeletonization,
        maxCompetitionsActive=maxCompetitionsActive,
        maxCompetitionRetries=maxCompetitionRetries,
        status="active",
        submissionId=submissionId,
        userEmail=userEmail,
    )
    row["_id"] = submissionId
    # get_db().submissions.insert_one(row)
    mongodb_data_api_request("insertOne", "submissions", document=row)
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
    maxCompetitionRetries: int,
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
        maxCompetitionRetries=maxCompetitionRetries,
        submissionId=submissionId,
        userEmail=userEmail,
    )
    # get_db().assays.insert_one(row)
    mongodb_data_api_request("insertOne", "assays", document=row)
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
    # get_db().assayResults.insert_one(row)
    mongodb_data_api_request("insertOne", "assayResults", document=row)


def has_assay_result(assayId: str) -> bool:
    # return bool(
    #     get_db().assayResults.count_documents(
    #         {"_id": assayId},
    #         limit=1,
    #     ),
    # )
    result = mongodb_data_api_request(
        "findOne", "assayResults", filter={"_id": assayId}
    )
    return result.get("document", None) is not None


def get_submission_assay_results(submissionId: str) -> list[dict]:
    # return list(
    #     get_db().assayResults.find(
    #         {"submissionId": submissionId},
    #     ),
    # )
    result = mongodb_data_api_request(
        "find", "assayResults", filter={"submissionId": submissionId}
    )
    return result.get("documents", [])


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
    # get_db().competitions.insert_one(row)
    mongodb_data_api_request("insertOne", "competitions", document=row)
    return row["_id"]


def add_competition_result(
    assayId: str,
    competitionId: str,
    numKnockoutSites: int,
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
            numKnockoutSites=numKnockoutSites,
            resultUpdatesElapsed=resultUpdatesElapsed,
            resultNumAlpha=resultNumAlpha,
            resultNumBeta=resultNumBeta,
            submissionId=submissionId,
            userEmail=userEmail,
            _id=competitionId,
        )
        # get_db().competitionResults.insert_one(row)
        mongodb_data_api_request(
            "insertOne", "competitionResults", document=row
        )
        return True


def has_competition_result(competitionId: str) -> bool:
    # return bool(
    #     get_db().competitionResults.count_documents(
    #         {"_id": competitionId},
    #         limit=1,
    #     ),
    # )
    result = mongodb_data_api_request(
        "findOne", "competitionResults", filter={"_id": competitionId}
    )
    return result.get("document", None) is not None


# cleanup =====================================================================
def purge_submission(submissionId: str):
    # for collection in get_db().list_collection_names():
    #     get_db()[collection].delete_many({"submissionId": submissionId})
    collections = [
        "submissions",
        "assays",
        "assayResults",
        "competitions",
        "competitionResults",
    ]
    for collection in collections:
        mongodb_data_api_request(
            "deleteMany", collection, filter={"submissionId": submissionId}
        )


def purge_testing():
    # for collection in get_db().list_collection_names():
    #     get_db()[collection].delete_many({"knockemRunmode": "testing"})
    collections = [
        "submissions",
        "assays",
        "assayResults",
        "competitions",
        "competitionResults",
    ]
    for collection in collections:
        mongodb_data_api_request(
            "deleteMany", collection, filter={"knockemRunmode": "testing"}
        )
