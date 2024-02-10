import json

from .. import orchestration as orch
from ...common import records as rec


def add_competition(
    assayDocument: dict,
    genomeIdAlpha: str,
    genomeIdBeta: str,
    knockoutSites: str,
    competitionDesignation: dict,
):
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
