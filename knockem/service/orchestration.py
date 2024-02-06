import functools
import os
import typing
import warnings

import dataset

from .meta import with_common_columns


@functools.lru_cache
def get_db() -> dataset.DataBase:
    if "PYTEST_CURRENT_TEST" in os.environ:
        return dataset.connect("sqlite:///knockem-testing.db")
    else:
        # Default Redis connection
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


# submissions =================================================================
def add_submission(
    competitionTimeoutSeconds: int,
    containerEnv: str,
    containerImage: str,
    genomeId: str,
    hasAssayDoseCalibration: bool,
    hasAssayDoseTitration: bool,
    hasAssayNulldist: bool,
    hasAssaySkeletonization: bool,
    maxCompetitionsActive: int,
    maxCompetitionsFail: int,
    submissionId: str,
    userEmail: str,
) -> None:
    row = with_common_columns(
        competitionTimeoutSeconds=competitionTimeoutSeconds,
        containerEnv=containerEnv,
        containerImage=containerImage,
        genomeId=genomeId,
        hasAssayDoseCalibration=hasAssayDoseCalibration,
        hasAssayDoseTitration=hasAssayDoseTitration,
        hasAssayNulldist=hasAssayNulldist,
        hasAssaySkeletonization=hasAssaySkeletonization,
        maxCompetitionsActive=maxCompetitionsActive,
        maxCompetitionsFail=maxCompetitionsFail,
        status="active",
        submissionId=submissionId,
        userEmail=userEmail,
    )
    with get_db() as tx:
        table = get_submissions_table()
        tx[table].insert(row)


def completeSubmission(submissionId: str) -> None:
    if depends_on_unresolved(dependedById=submissionId):
        warnings.warn(
            f"Submission {submissionId} has unresolved dependencies "
            "but is being completed.",
        )
    with get_db() as tx:
        tx[get_submissions_table()].delete(id=submissionId)
        tx[get_assays_table()].delete(submissionId=submissionId)
        tx[get_competitions_table()].delete(submissionId=submissionId)


# assays ======================================================================
def activate_assay(assayId: str) -> None:
    table = get_assays_table()
    with get_db() as tx:
        tx[table].update(dict(id=assayId, status="active"), ["id"])


def complete_assay(assayId: str) -> None:
    if depends_on_unresolved(dependedById=assayId):
        raise RuntimeError(
            f"Assay {assayId} has unresolved dependencies "
            "but is being completed.",
        )
    table = get_assays_table()
    with get_db() as tx:
        resolve_dependencies_on(dependsOnId=assayId)
        tx[table].delete(id=assayId)


def enqueue_assay(
    assayId: int,
    assayType: str,
    competitionTimeoutSeconds: int,
    containerEnv: str,
    containerImage: str,
    dependsOnIds: list[str],
    genomeId: str,
    maxCompetitionsActive: int,
    maxCompetitionsFail: int,
    submissionId: str,
    userEmail: str,
) -> None:
    row = with_common_columns(
        assayId=assayId,
        assayType=assayType,
        competitionTimeoutSeconds=competitionTimeoutSeconds,
        containerEnv=containerEnv,
        containerImage=containerImage,
        genomeId=genomeId,
        maxCompetitionsActive=maxCompetitionsActive,
        maxCompetitionsFail=maxCompetitionsFail,
        submissionId=submissionId,
        status="pending",
        userEmail=userEmail,
    )
    with get_db() as tx:
        tx[get_assays_table()].insert(row)
        add_dependency(dependedById=submissionId, dependsOnId=row["id"])
        for dependsOnId in dependsOnIds:
            add_dependency(dependedById=row["id"], dependsOnId=dependsOnId)


# competitions ================================================================
def activate_competition(competitionId: str) -> None:
    table = get_competitions_table()
    with get_db() as tx:
        tx[table].update(dict(id=competitionId, status="active"), ["id"])


def enqueue_competition(
    assayId: str,
    competitionId: str,
    competitionTimeoutSeconds: int,
    containerEnv: str,
    containerImage: str,
    genomeIdAlpha: str,
    genomeIdBeta: str,
    knockoutSites: str,
    maxCompetitionsActive: int,
    maxCompetitionsFail: int,
    submissionId: str,
    userEmail: str,
) -> None:
    row = with_common_columns(
        assayId=assayId,
        competitionId=competitionId,
        competitionTimeoutSeconds=competitionTimeoutSeconds,
        containerEnv=containerEnv,
        containerImage=containerImage,
        genomeIdAlpha=genomeIdAlpha,
        genomeIdBeta=genomeIdBeta,
        knockoutSites=knockoutSites,
        maxCompetitionsActive=maxCompetitionsActive,
        maxCompetitionsFail=maxCompetitionsFail,
        status="pending",
        submissionId=submissionId,
        userEmail=userEmail,
    )
    with get_db() as tx:
        tx[get_competitions_table()].insert(row)
        add_dependency(dependedById=assayId, dependsOnId=row["id"])


def complete_competition(competitionId: str) -> None:
    table = get_competitions_table()
    with get_db() as tx:
        tx[table].update(dict(id=competitionId, status="completed"), ["id"])
        resolve_dependencies_on(dependsOnId=competitionId)


def fail_competition(competitionId: str) -> None:
    table = get_competitions_table()
    with get_db() as tx:
        tx[table].update(dict(id=competitionId, status="failed"), ["id"])


# dependencies =================================================================
def add_dependency(dependedById: str, dependsOnId: str) -> str:
    row = with_common_columns(
        "dependencyId", dependedById=dependedById, dependsOnId=dependsOnId
    )
    table = get_dependencies_table()
    with get_db() as tx:
        tx[table].insert(row)
    return row["dependencyId"]


def depends_on_unresolved(dependedById: str) -> bool:
    table = get_dependencies_table()
    with get_db() as tx:
        return bool(tx[table].find(dependedById=dependedById))


def resolve_dependencies_on(dependsOnId: str) -> None:
    table = get_dependencies_table()
    with get_db() as tx:
        tx[table].delete(dependsOnId=dependsOnId)


# counters ====================================================================
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


# cleanup =====================================================================
def purge_submission(submissionId: str) -> None:
    with get_db() as tx:
        for table in tx.tables:
            table.delete(submissionId=submissionId)


def purge_testing() -> None:
    with get_db() as tx:
        for table in tx.tables:
            table.delete(knockemRunmode="testing")
