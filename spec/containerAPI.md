## `knockem_apply_knockout`

args:
- `sites`... (int)

stdin:
- `genome content` (str)

stdout: (expected)
- `knocked out genome content` (str)

env:
- any custom environment settings passed via `containerEnv`

invocation:
```
singularity run {containerImage} \
    knockem__apply_knockout {site1} {site2} ... \
    --env KNOCKEM_CUSTOM_ENV1='{customEnv1}' ...
    < {genomeContent} > output.genome
```

## `knockem_count_sites`

args: none

stdin:
- `genome content` (str)

stdout: (expected)
- `num genome sites` (int)

env:
- any custom environment settings passed via `containerEnv`

invocation:
```
singularity run {containerImage} \
    knockem_count_sites \
    --env KNOCKEM_CUSTOM_ENV1='{customEnv1}' ...
    < {genomeContent} > output.count
```

## `knockem_compete_two`

args: none

env:
- `KNOCKEM_ASSAY_ID` (str)
- `KNOCKEM_COMPETITION_ID` (str)
- `KNOCKEM_COMPETITION_ATTEMPT_ID` (str)
- `KNOCKEM_RECORDS_URI` (str)
- `KNOCKEM_RECORDS_CREDENTIAL` (str)
- `KNOCKEM_GENOME_ID_ALPHA` (str)
- `KNOCKEM_GENOME_ID_BETA` (str)
- `KNOCKEM_RUNMODE` (str)
- `KNOCKEM_SUBMISSION_ID` (str)
- `KNOCKEM_USER_EMAIL` (str)
- any custom environment settings passed via `containerEnv`

invocation:
```
singularity run {containerImage} \
    knockem_compete_two \
    --env KNOCKEM_ASSAY_ID='{assayId}' \
    --env KNOCKEM_COMPETITION_ID='{competitionId}' \
    --env KNOCKEM_COMPETITION_ATTEMPT_ID='{competitionAttemptId}' \
    --env KNOCKEM_RECORDS_URI='{databaseUri}' \
    --env KNOCKEM_RECORDS_CREDENTIAL='{databaseCredential}' \
    --env KNOCKEM_GENOME_ID_ALPHA='{genomeIdAlpha}' \
    --env KNOCKEM_GENOME_ID_BETA='{genomeIdBeta}' \
    --env KNOCKEM_SUBMISSION_ID='{submissionId}' \
    --env KNOCKEM_RUNMODE='{knockemRunmode}' \
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
