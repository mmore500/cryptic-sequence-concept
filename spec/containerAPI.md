## `knockem_knockout`

args:
- `sites`... (int)

stdin:
- `genome content` (str)

stdout: (expected)
- `knocked out genome content` (str)

invocation:
```
singularity run {containerImage} \
    knockem_knockout {site1} {site2} ... \
    < {genomeContent} > output.genome
```

## `knockem_compete`

env:
- `KNOCKEM_ASSAY_ID` (str)
- `KNOCKEM_COMPETITION_ID` (str)
- `KNOCKEM_COMPETITION_ATTEMPT_ID` (str)
- `KNOCKEM_DATABASE_URI` (str)
- `KNOCKEM_DATABASE_CREDENTIAL` (str)
- `KNOCKEM_EPHEMERAL_GENOME_IDS` (space-separated str with ephemeral genome IDs)
- `KNOCKEM_GENOME_ID_ALPHA` (str)
- `KNOCKEM_GENOME_ID_BETA` (str)
- `KNOCKEM_REVISION` (str)
- `KNOCKEM_SUBMISSION_ID` (str)
- `KNOCKEM_USER_EMAIL` (str)
- any custom environment settings passed via `containerEnv`

invocation:
```
singularity run {containerImage} \
    knockem_compete "{genomeIdAlpha}" "{genomeIdBeta}" \
    --env KNOCKEM_ASSAY_ID='{assayId}' \
    --env KNOCKEM_COMPETITION_ID='{competitionId}' \
    --env KNOCKEM_COMPETITION_ATTEMPT_ID='{competitionAttemptId}' \
    --env KNOCKEM_DATABASE_URI='{databaseUri}' \
    --env KNOCKEM_DATABASE_CREDENTIAL='{databaseCredential}' \
    --env KNOCKEM_REVISION='{revision}' \
    --env KNOCKEM_SUBMISSION_ID='{submissionId}' \
    --env KNOCKEM_USER_EMAIL='{userEmail}' \
    --env KNOCKEM_CUSTOM_ENV1='{customEnv1}' ...
```

responsibilities:
- get genomes from database
    - invoke `python3 -m knockem.cli fetch-genome "{genomeIdAlpha}"` and `python3 -m knockem.cli fetch-genome "{genomeIdBeta}"`
- run competition
- upload competition results to database to `competitionAttemptResults`
    - invoke `knockem.cli report-competition "{updatesElapsed}" "{numAlpha}" "{numBeta}"`
    - will only upload competition result if it is not present
    - on success, deletes ephemeral genomes from database
