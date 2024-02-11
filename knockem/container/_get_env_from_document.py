import uuid


def get_env_from_document(document: dict) -> dict:
    res = {
        "KNOCKEM_CONTAINER_IMAGE": document["containerImage"],
        "KNOCKEM_GENOME_ID_ALPHA": document["genomeIdAlpha"],
        "KNOCKEM_RUNMODE": document["knockemRunmode"],
        "KNOCKEM_SUBMISSION_ID": document["submissionId"],
        "KNOCKEM_USER_EMAIL": document["userEmail"],
    }

    if "assayId" in document:
        res["KNOCKEM_ASSAY_ID"] = document["assayId"]

    if "competitionId" in document:
        res["KNOCKEM_COMPETITION_ID"] = document["competitionId"]
        res["KNOCKEM_COMPETITION_ATTEMPT_ID"] = str(uuid.uuid4())
        res["KNOCKEM_GENOME_ID_BETA"] = document["genomeIdBeta"]
        res["KNOCKEM_NUM_KNOCKOUT_SITES"] = len(
            document["knockoutSites"].split(),
        )

    return res
