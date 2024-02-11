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
singularity run \
    --env KNOCKEM_CUSTOM_ENV1='{customEnv1}' ... \
    {containerImage} \
    knockem__apply_knockout {site1} {site2} ... \
    < {genomeContent} > output.genome
```

responsibilities: (**end user implements**)
- read genome content from stdin
- take integer site id's as script args (i.e., bash `$@`)
- print genome content with knockouts at site id's applied


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
singularity run \
    --env KNOCKEM_CUSTOM_ENV1='{customEnv1}' ... \
    {containerImage} \
    knockem_count_sites \
    < {genomeContent} > output.count
```

responsibilities: (**end user implements**)
- read genome content from stdin
- print integer count of sites in genome

## `knockem_compete_two`

args: none

env:
- `KNOCKEM_ASSAY_ID` (str)
- `KNOCKEM_COMPETITION_ID` (str)
- `KNOCKEM_COMPETITION_ATTEMPT_ID` (str)
- `KNOCKEM_RECORDS_URI` (str), contains credential
- `KNOCKEM_GENOME_ID_ALPHA` (str)
- `KNOCKEM_GENOME_ID_BETA` (str)
- `KNOCKEM_RUNMODE` (str)
- `KNOCKEM_SUBMISSION_ID` (str)
- `KNOCKEM_USER_EMAIL` (str)
- any custom environment settings passed via `containerEnv`

invocation:
```
singularity run \
    --env KNOCKEM_ASSAY_ID='{assayId}' \
    --env KNOCKEM_COMPETITION_ID='{competitionId}' \
    --env KNOCKEM_COMPETITION_ATTEMPT_ID='{competitionAttemptId}' \
    --env KNOCKEM_RECORDS_URI='{databaseUri}' \
    --env KNOCKEM_GENOME_ID_ALPHA='{genomeIdAlpha}' \
    --env KNOCKEM_GENOME_ID_BETA='{genomeIdBeta}' \
    --env KNOCKEM_SUBMISSION_ID='{submissionId}' \
    --env KNOCKEM_RUNMODE='{knockemRunmode}' \
    --env KNOCKEM_USER_EMAIL='{userEmail}' \
    --env KNOCKEM_CUSTOM_ENV1='{customEnv1}' ... \
    {containerImage} \
    knockem_compete_two
```

responsibilities:
- get genomes from database (**end user calls knockem.cli from within container**)
    - invoke `python3 -m knockem.cli fetch-genome "{genomeIdAlpha}"` and `python3 -m knockem.cli fetch-genome "{genomeIdBeta}"`
- run competition (**end user implements entirely**)
- upload competition results to database to `competitionAttemptResults` (**end user calls knockem.cli from within container**)
    - invoke `python3 -m knockem.cli report-competition "{updatesElapsed}" "{numAlpha}" "{numBeta}"`
    - will only upload competition result if it is not present
    - on success, deletes ephemeral genomes from database
