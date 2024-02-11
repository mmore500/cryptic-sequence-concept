import functools
import time
import typing
import warnings

import dataset

from ..common.meta import get_runmode, with_common_columns


def _get_time() -> int:
    return time.time_ns() // 1000000000


@functools.lru_cache
def get_db() -> dataset.Database:
    if get_runmode() == "testing":
        return dataset.connect("sqlite:///knockem-testing.db")
    else:
        return dataset.connect("sqlite:///knockem-production.db")


# tables ======================================================================
def get_assays_table() -> str:
    return "assays"


def get_competitions_table() -> str:
    return "competitions"


def get_dependencies_table() -> str:
    return "dependencies"


def get_submissions_table() -> str:
    return "submissions"


def get_api_tokens_table() -> str:
    return "users"


# submissions =================================================================
def activate_submission(submissionId: str) -> None:
    table = get_submissions_table()
    with get_db() as tx:
        tx[table].update(
            dict(
                activationTimestamp=_get_time(),
                submissionId=submissionId,
                status="active",
            ),
            ["submissionId"],
        )


def enqueue_submission(
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
) -> None:
    row = with_common_columns(
        activationTimestamp=0,
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
        status="pending",
        submissionId=submissionId,
        userEmail=userEmail,
    )
    with get_db() as tx:
        table = get_submissions_table()
        tx[table].insert(row)


def complete_submission(submissionId: str) -> None:
    if depends_on_unresolved(dependedById=submissionId):
        warnings.warn(
            f"Submission {submissionId} has unresolved dependencies "
            "but is being completed.",
        )
    with get_db() as tx:
        tx[get_submissions_table()].delete(submissionId=submissionId)
        tx[get_assays_table()].delete(submissionId=submissionId)
        tx[get_competitions_table()].delete(submissionId=submissionId)


def get_submission_document(submissionId: str) -> dict:
    table = get_submissions_table()
    with get_db() as tx:
        return tx[table].find_one(submissionId=submissionId)


def iter_active_submissionIds() -> typing.List[str]:
    table = get_submissions_table()
    with get_db() as tx:
        for row in tx[table].find(status="active"):
            yield row["submissionId"]


def iter_pending_submissionIds() -> typing.List[str]:
    table = get_submissions_table()
    with get_db() as tx:
        for row in tx[table].find(status="pending"):
            yield row["submissionId"]


def has_submission(submissionId: str) -> bool:
    table = get_submissions_table()
    with get_db() as tx:
        return bool(tx[table].count(submissionId=submissionId))


# assays ======================================================================
def activate_assay(assayId: str) -> None:
    table = get_assays_table()
    with get_db() as tx:
        tx[table].update(dict(assayId=assayId, status="active"), ["assayId"])


def complete_assay(assayId: str) -> None:
    if depends_on_unresolved(dependedById=assayId):
        raise RuntimeError(
            f"Assay {assayId} has unresolved dependencies "
            "but is being completed.",
        )
    table = get_assays_table()
    with get_db() as tx:
        resolve_dependencies_on(dependsOnId=assayId)
        tx[table].delete(assayId=assayId)


def enqueue_assay(
    assayDesignation: dict,
    assayId: str,
    assayType: str,
    competitionTimeoutSeconds: int,
    containerEnv: str,
    containerImage: str,
    dependedByIds: list[str],
    dependsOnIds: list[str],
    genomeIdAlpha: str,
    maxCompetitionsActive: int,
    maxCompetitionRetries: int,
    submissionId: str,
    userEmail: str,
) -> None:
    row = with_common_columns(
        assayDesignation=assayDesignation,
        assayId=assayId,
        assayType=assayType,
        competitionTimeoutSeconds=competitionTimeoutSeconds,
        containerEnv=containerEnv,
        containerImage=containerImage,
        genomeIdAlpha=genomeIdAlpha,
        maxCompetitionsActive=maxCompetitionsActive,
        maxCompetitionRetries=maxCompetitionRetries,
        submissionId=submissionId,
        status="pending",
        userEmail=userEmail,
    )
    table = get_assays_table()
    with get_db() as tx:
        tx[table].insert(row)
        add_dependency(
            dependedById=submissionId,
            dependsOnId=row["assayId"],
            submissionId=submissionId,
            userEmail=userEmail,
        )
        for dependsOnId in dependsOnIds:
            add_dependency(
                dependedById=row["assayId"],
                dependsOnId=dependsOnId,
                submissionId=submissionId,
                userEmail=userEmail,
            )
        for dependedById in dependedByIds:
            add_dependency(
                dependedById=dependedById,
                dependsOnId=row["assayId"],
                submissionId=submissionId,
                userEmail=userEmail,
            )


def get_assay_document(assayId: str) -> dict:
    table = get_assays_table()
    with get_db() as tx:
        return tx[table].find_one(assayId=assayId)


def iter_active_assayIds() -> typing.Iterator[str]:
    table = get_assays_table()
    with get_db() as tx:
        for row in tx[table].find(status="active"):
            yield row["assayId"]


def iter_pending_assayIds() -> typing.Iterator[str]:
    table = get_assays_table()
    with get_db() as tx:
        for row in tx[table].find(status="pending"):
            yield row["assayId"]


def iter_submission_assayIds_of_type(
    submissionId: str, assayType: str
) -> typing.Iterator[str]:
    table = get_assays_table()
    with get_db() as tx:
        for row in tx[table].find(
            submissionId=submissionId, assayType=assayType
        ):
            yield row["assayId"]


# competitions ================================================================
def activate_competition(competitionId: str) -> None:
    table = get_competitions_table()
    with get_db() as tx:
        tx[table].update(
            dict(
                activationTimestamp=_get_time(),
                competitionId=competitionId,
                status="active",
            ),
            ["competitionId"],
        )


def requeue_competition(competitionId: str, retry: int) -> None:
    table = get_competitions_table()
    with get_db() as tx:
        tx[table].update(
            dict(
                competitionId=competitionId,
                competitionRetryCount=retry,
                status="pending",
            ),
            ["competitionId"],
        )


def enqueue_competition(
    assayId: str,
    competitionDesignation: str,
    competitionId: str,
    competitionTimeoutSeconds: int,
    containerEnv: str,
    containerImage: str,
    genomeIdAlpha: str,
    genomeIdBeta: str,
    knockoutSites: str,
    maxCompetitionsActive: int,
    maxCompetitionRetries: int,
    submissionId: str,
    userEmail: str,
) -> None:
    row = with_common_columns(
        activationTimestamp=0,
        assayId=assayId,
        competitionDesignation=competitionDesignation,
        competitionId=competitionId,
        competitionRetryCount=0,
        competitionTimeoutSeconds=competitionTimeoutSeconds,
        containerEnv=containerEnv,
        containerImage=containerImage,
        genomeIdAlpha=genomeIdAlpha,
        genomeIdBeta=genomeIdBeta,
        knockoutSites=knockoutSites,
        maxCompetitionsActive=maxCompetitionsActive,
        maxCompetitionRetries=maxCompetitionRetries,
        status="pending",
        submissionId=submissionId,
        userEmail=userEmail,
    )
    with get_db() as tx:
        tx[get_competitions_table()].insert(row)
        add_dependency(
            dependedById=assayId,
            dependsOnId=row["competitionId"],
            submissionId=submissionId,
            userEmail=userEmail,
        )


def complete_competition(competitionId: str) -> None:
    table = get_competitions_table()
    with get_db() as tx:
        tx[table].update(
            dict(competitionId=competitionId, status="completed"),
            ["competitionId"],
        )
        resolve_dependencies_on(dependsOnId=competitionId)


def fail_competition(competitionId: str) -> None:
    table = get_competitions_table()
    with get_db() as tx:
        tx[table].update(
            dict(competitionId=competitionId, status="failed"),
            ["competitionId"],
        )
    raise RuntimeError(f"Competition {competitionId} has failed.")


def get_competition_document(competitionId: str) -> dict:
    table = get_competitions_table()
    with get_db() as tx:
        return tx[table].find_one(competitionId=competitionId)


def is_competition_completed(competitionId: str) -> bool:
    return get_competition_document["status"] == "completed"


def iter_active_competitionIds() -> typing.Iterator[str]:
    table = get_competitions_table()
    with get_db() as tx:
        for row in tx[table].find(status="active"):
            yield row["competitionId"]


def iter_pending_competitionIds() -> typing.Iterator[str]:
    table = get_competitions_table()
    with get_db() as tx:
        for row in tx[table].find(status="pending"):
            yield row["competitionId"]


def iter_assay_competitionIds(assayId: str) -> typing.Iterator[str]:
    table = get_competitions_table()
    with get_db() as tx:
        for row in tx[table].find(assayId=assayId):
            yield row["competitionId"]


# dependencies =================================================================
def add_dependency(
    dependedById: str, dependsOnId: str, submissionId: str, userEmail: str
) -> str:
    row = with_common_columns(
        "dependencyId",
        dependedById=dependedById,
        dependsOnId=dependsOnId,
        submissionId=submissionId,
        userEmail=userEmail,
    )
    table = get_dependencies_table()
    with get_db() as tx:
        tx[table].insert(row)
    return row["dependencyId"]


def depends_on_unresolved(dependedById: str) -> bool:
    table = get_dependencies_table()
    with get_db() as tx:
        return bool(tx[table].count(dependedById=dependedById))


def resolve_dependencies_on(dependsOnId: str) -> None:
    table = get_dependencies_table()
    with get_db() as tx:
        tx[table].delete(dependsOnId=dependsOnId)


# counters ====================================================================
def get_num_dependencies(submissionId: str) -> int:
    table = get_dependencies_table()
    with get_db() as tx:
        return tx[table].count(submissionId=submissionId)


def get_num_active_assays(submissionId: str) -> int:
    table = get_assays_table()
    with get_db() as tx:
        return tx[table].count(submissionId=submissionId, status="active")


def get_num_completed_assays(submissionId: str) -> int:
    table = get_assays_table()
    with get_db() as tx:
        return tx[table].count(submissionId=submissionId, status="completed")


def get_num_failed_assays(submissionId: str) -> int:
    table = get_assays_table()
    with get_db() as tx:
        return tx[table].count(submissionId=submissionId, status="failed")


def get_num_pending_assays(submissionId: str) -> int:
    table = get_assays_table()
    with get_db() as tx:
        return tx[table].count(submissionId=submissionId, status="pending")


def get_num_active_competitions(submissionId: str) -> int:
    table = get_competitions_table()
    with get_db() as tx:
        return tx[table].count(submissionId=submissionId, status="active")


def get_num_completed_competitions(submissionId: str) -> int:
    table = get_competitions_table()
    with get_db() as tx:
        return tx[table].count(submissionId=submissionId, status="completed")


def get_num_failed_competitions(submissionId: str) -> int:
    table = get_competitions_table()
    with get_db() as tx:
        return tx[table].count(submissionId=submissionId, status="failed")


def get_num_pending_competitions(submissionId: str) -> int:
    table = get_competitions_table()
    with get_db() as tx:
        return tx[table].count(submissionId=submissionId, status="pending")


def get_num_assay_competitions(assayId: str) -> int:
    table = get_competitions_table()
    with get_db() as tx:
        return tx[table].count(assayId=assayId)


# cleanup =====================================================================
def purge_submission(submissionId: str) -> None:
    with get_db() as tx:
        for table in tx.tables:
            tx[table].delete(submissionId=submissionId)


def purge_testing() -> None:
    with get_db() as tx:
        for table in tx.tables:
            tx[table].delete(knockemRunmode="testing")


def purge_work() -> None:
    with get_db() as tx:
        for table in [
            get_assays_table(),
            get_competitions_table(),
            get_dependencies_table(),
            get_submissions_table(),
        ]:
            tx[table].delete()


# api tokens ==================================================================
def add_api_token(userEmail: str) -> str:
    row = with_common_columns("apiToken", userEmail=userEmail)
    table = get_api_tokens_table()
    with get_db() as tx:
        tx[table].insert(row)
    return row["apiToken"]


def has_api_token(apiToken: str) -> bool:
    table = get_api_tokens_table()
    with get_db() as tx:
        return bool(tx[table].count(apiToken=apiToken))
