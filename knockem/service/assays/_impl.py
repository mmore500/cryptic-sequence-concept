import json

from .. import orchestration as orch
from ...common import records as rec
from ...container import apply_knockout


def add_competition(
    assayDocument: dict,
    genomeIdAlpha: str,
    genomeIdBeta: str,
    knockoutSites: str,
    competitionDesignation: dict,
) -> None:
    competitionId = rec.add_competition(
        assayId=assayDocument["assayId"],
        competitionDesignation=competitionDesignation,
        genomeIdAlpha=genomeIdAlpha,
        genomeIdBeta=genomeIdBeta,
        knockoutSites=knockoutSites,
        submissionId=assayDocument["submissionId"],
        userEmail=assayDocument["userEmail"],
    )
    orch.enqueue_competition(
        assayId=assayDocument["assayId"],
        competitionDesignation=json.dumps(competitionDesignation),
        competitionId=competitionId,
        competitionTimeoutSeconds=assayDocument["competitionTimeoutSeconds"],
        containerEnv=assayDocument["containerEnv"],
        containerImage=assayDocument["containerImage"],
        genomeIdAlpha=genomeIdAlpha,
        genomeIdBeta=genomeIdBeta,
        knockoutSites=knockoutSites,
        maxCompetitionsActive=assayDocument["maxCompetitionsActive"],
        maxCompetitionRetries=assayDocument["maxCompetitionRetries"],
        submissionId=assayDocument["submissionId"],
        userEmail=assayDocument["userEmail"],
    )


def make_knockout_genome_id(
    assayDocument: dict,
    genomeDocument: dict,
    knockoutSites: str,
) -> str:
    knockedOutContent = apply_knockout(
        genomeContent=genomeDocument["genomeContent"],
        knockoutSites=knockoutSites,
        containerEnv=assayDocument["containerEnv"],
        containerImage=assayDocument["containerImage"],
    )
    return rec.add_genome(
        containerEnv=assayDocument["containerEnv"],
        containerImage=assayDocument["containerImage"],
        genomeContent=knockedOutContent,
        isEphemeral=True,
        submissionId=assayDocument["submissionId"],
        userEmail=assayDocument["userEmail"],
    )
