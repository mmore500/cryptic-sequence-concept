import functools
import json
import logging
import os
import typing
import warnings

from pymongo import MongoClient
from pymongo.database import Database as MongoDatabase
import requests

from ..auxlib._is_slurm_job import is_slurm_job
from ..container import count_sites
from .meta import with_common_columns


@functools.lru_cache
def get_db() -> typing.Optional[MongoDatabase]:
    env_key = "KNOCKEM_RECORDS_URI"
    if env_key not in os.environ:
        warnings.warn(
            f"Environment var {env_key} is not set, using MongoDB Data API.",
        )
        return None
    elif is_slurm_job():
        logging.info("SLURM job detected. Using MongoDB Data API.")
        return None

    uri = os.environ["KNOCKEM_RECORDS_URI"]
    logging.info(f"Connecting to {uri}")
    return MongoClient(uri).knockem


# Helper function for MongoDB Data API requests
def mongodb_data_api_request(
    action: str,
    collection: str,
    document: typing.Optional[dict] = None,
    filter: typing.Optional[dict] = None,
    update: typing.Optional[dict] = None,
    projection: typing.Optional[dict] = None,
) -> dict:
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
    containerEnv: str,
    containerImage: str,
    genomeContent: str,
    isEphemeral: bool,
    submissionId: str,
    userEmail: str,
) -> str:
    row = with_common_columns(
        "genomeId",
        "_id",
        containerEnv=containerEnv,
        containerImage=containerImage,
        genomeContent=genomeContent,
        genomeNumSites=count_sites(genomeContent, containerEnv, containerImage),
        isEphemeral=isEphemeral,
        submissionId=submissionId,
        userEmail=userEmail,
    )
    if get_db() is None:
        mongodb_data_api_request("insertOne", "genomes", document=row)
    else:
        get_db().genomes.insert_one(row)
    return row["genomeId"]


def delete_genome_document(genomeId: str) -> None:
    if get_db() is None:
        mongodb_data_api_request(
            "deleteOne", "genomes", filter={"genomeId": genomeId}
        )
    else:
        get_db().genomes.delete_one({"genomeId": genomeId})


def get_genome_document(genomeId: str) -> dict:
    if get_db() is None:
        result = mongodb_data_api_request(
            "findOne", "genomes", filter={"genomeId": genomeId}
        )
        return result.get("document")
    else:
        return get_db().genomes.find_one({"genomeId": genomeId})


def is_genome_ephemeral(genomeId: str) -> bool:
    if get_db() is None:
        result = mongodb_data_api_request(
            "findOne",
            "competitionResults",
            filter={"genomeId": genomeId, "isEphemeral": True},
        )
        return result.get("document", None) is not None
    else:
        return bool(
            get_db().competitionResults.count_documents(
                {"genomeId": genomeId, "isEphemeral": True},
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
    hasAssayScreenCritical: bool,
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
        hasAssayScreenCritical=hasAssayScreenCritical,
        hasAssaySkeletonization=hasAssaySkeletonization,
        maxCompetitionsActive=maxCompetitionsActive,
        maxCompetitionRetries=maxCompetitionRetries,
        status="active",
        submissionId=submissionId,
        userEmail=userEmail,
    )
    row["_id"] = submissionId
    if get_db() is None:
        mongodb_data_api_request("insertOne", "submissions", document=row)
    else:
        get_db().submissions.insert_one(row)

    return row["_id"]


def has_submission(submissionId: str) -> bool:
    if get_db() is None:
        result = mongodb_data_api_request(
            "findOne", "submissions", filter={"_id": submissionId}
        )
        return result.get("document", None) is not None
    else:
        return bool(
            get_db().submissions.count_documents(
                {"_id": submissionId},
                limit=1,
            ),
        )


# assays ======================================================================
def add_assay(
    assayDesignation: dict,
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
        assayDesignation=assayDesignation,
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
    if get_db() is None:
        mongodb_data_api_request("insertOne", "assays", document=row)
    else:
        get_db().assays.insert_one(row)
    return row["_id"]


def add_assay_result(
    assayId: str,
    assayResult: dict,
    assayType: str,
    submissionId: str,
    userEmail: str,
) -> None:
    row = with_common_columns(
        assayId=assayId,
        assayResult=assayResult,
        assayType=assayType,
        submissionId=submissionId,
        userEmail=userEmail,
        _id=assayId,
    )
    if get_db() is None:
        mongodb_data_api_request("insertOne", "assayResults", document=row)
    else:
        get_db().assayResults.insert_one(row)


def has_assay_result(assayId: str) -> bool:
    if get_db() is None:
        result = mongodb_data_api_request(
            "findOne", "assayResults", filter={"_id": assayId}
        )
        return result.get("document", None) is not None
    else:
        return bool(
            get_db().assayResults.count_documents(
                {"_id": assayId},
                limit=1,
            ),
        )


def does_submission_have_assay_result_of_type(
    submissionId: str,
    assayType: str,
) -> bool:
    if get_db() is None:
        result = mongodb_data_api_request(
            "findOne",
            "assayResults",
            filter={"assayType": assayType, "submissionId": submissionId},
        )
        return result.get("document", None) is not None
    else:
        return bool(
            get_db().assayResults.count_documents(
                {"assayType": assayType, "submissionId": submissionId},
                limit=1,
            ),
        )


def get_submission_assay_results(submissionId: str) -> list[dict]:
    if get_db() is None:
        result = mongodb_data_api_request(
            "find", "assayResults", filter={"submissionId": submissionId}
        )
        return result.get("documents", [])
    else:
        return list(
            get_db().assayResults.find(
                {"submissionId": submissionId},
            ),
        )


def get_submission_assay_result_of_type(
    submissionId: str, assayType: str
) -> typing.Optional[dict]:
    if get_db() is None:
        result = mongodb_data_api_request(
            "findOne",
            "assayResults",
            filter={"submissionId": submissionId, "assayType": assayType},
        )
        return result.get("document", None)
    else:
        return get_db().assayResults.find_one(
            {"submissionId": submissionId, "assayType": assayType},
        )


# competitios =================================================================
def add_competition(
    assayId: str,
    competitionDesignation: dict,
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
        competitionDesignation=competitionDesignation,
        genomeIdAlpha=genomeIdAlpha,
        genomeIdBeta=genomeIdBeta,
        knockoutSites=knockoutSites,
        numKnockoutSites=len(knockoutSites.split()),
        submissionId=submissionId,
        userEmail=userEmail,
    )
    if get_db() is None:
        mongodb_data_api_request("insertOne", "competitions", document=row)
    else:
        get_db().competitions.insert_one(row)
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
        if get_db() is None:
            mongodb_data_api_request(
                "insertOne", "competitionResults", document=row
            )
        else:
            get_db().competitionResults.insert_one(row)
        return True


def get_competition_document(competitionId: str):
    if get_db() is None:
        result = mongodb_data_api_request(
            "findOne", "competitions", filter={"competitionId": competitionId}
        )
        return result.get("document")
    else:
        return get_db().competitions.find_one({"competitionId": competitionId})


def get_assay_competition_results(assayId: str) -> list[dict]:
    if get_db() is None:
        result = mongodb_data_api_request(
            "find", "competitionresults", filter={"assayId": assayId}
        )
        return result.get("documents", [])
    else:
        return list(
            get_db().competitionResults.find(
                {"assayId": assayId},
            ),
        )


def has_competition_result(competitionId: str) -> bool:
    if get_db() is None:
        result = mongodb_data_api_request(
            "findOne", "competitionResults", filter={"_id": competitionId}
        )
        return result.get("document", None) is not None
    else:
        return bool(
            get_db().competitionResults.count_documents(
                {"_id": competitionId},
                limit=1,
            ),
        )


# cleanup =====================================================================
def purge_submission(submissionId: str):
    if get_db() is None:
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
    else:
        for collection in get_db().list_collection_names():
            get_db()[collection].delete_many({"submissionId": submissionId})


def purge_testing():
    if get_db() is None:
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
    else:
        for collection in get_db().list_collection_names():
            get_db()[collection].delete_many({"knockemRunmode": "testing"})
