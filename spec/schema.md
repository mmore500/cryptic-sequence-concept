## noSQL database

for job report-back and record keeping

### `genomes`
- `datetime`: string, ISO 8601
- `genomeContent`: string
- `genomeId`: string, RFC 4122 UUID
- `isEphemeral`: boolean (should genome be deleted after download?)
    - should genome be deleted after use?
- `knockemRevision`: string, short git commit hash
- `knockemRunmode`: string, production or testing
- `knockemVersion`: string, semantic version
- `numSites`: int
- `userEmail`: string, email

### `submissions`
- `assayIds`: list of strings, assay UUIDs
- `assayTypes`: list of strings (enum)
- `competitionTimeoutSeconds`: int
- `containerEnv`: map of string to string
- `containerImage`: string, Docker Hub image name or a registry name
- `datetime`: string, ISO 8601
- `genomeIdAlpha`: string
- `id`: string, RFC 4122 UUID
- `knockemRevision`: string, short git commit hash
- `knockemRunmode`: string, production or testing
- `knockemVersion`: string, semantic version
- `maxCompetitionsActive`: int
- `maxCompetitionsFail`: int
- `userEmail`: string, email

### `assays`
- `assayType`: string (enum)
- `competitionIDs`: list of strings, competition UUIDs
- `containerEnv`: map of string to string
- `containerImage`: string, Docker Hub image name or a registry name
- `datetime`: string, ISO 8601
- `id`: string, RFC 4122 UUID
- `knockemRevision`: string, short git commit hash
- `knockemRunmode`: string, production or testing
- `knockemVersion`: string, semantic version
- `submissionId`: string, submission UUID
- `userEmail`: string, email

### `assayResults`
- `datetime`: string, ISO 8601
- `id`: string, RFC 4122 UUID (corresponding to entry in `assays`)
- `knockemRevision`: string, short git commit hash
- `knockemVersion`: string, semantic version
- `assayResult`: JSON

### `competitions`
- `assayId`: string, assay UUID
- `datetime`: string, ISO 8601
- `id`: string, RFC 4122 UUID
- `knockemRevision`: string, short git commit hash
- `knockemRunmode`: string, production or testing
- `knockemVersion`: string, semantic version
- `knockoutSites`: list of int
- `submissionId`: string, submission UUID
- `userEmail`: string, email

### `competitionResults`
- `assayId`: string, assay UUID
- `competitionAttemptId`: string, RFC 4122 UUID
- `datetime`: string, ISO 8601
- `id`: string, RFC 4122 UUID (corresponding to entry in `competitions`)
- `knockemRevision`: string, short git commit hash
- `knockemRunmode`: string, production or testing
- `knockemVersion`: string, semantic version
- `knockoutSites`: list of int
- `numKnockoutSites`: int
- `result`:
    - `updatesElapsed`: numeric
    - `numAlpha`: int
    - `numBeta`: int
- `submissionId`: string, submission UUID
- `userEmail`: string, email

## sqlite database

for server job orchestration

### `submissions`
- `assayIds`: list of strings, assay UUIDs
- `competitionTimeoutSeconds`: int
- `containerEnv`: map of string to string
- `containerImage`: string, Docker Hub image name or a registry name
- `datetime`: string, ISO 8601
- `genomeIdAlpha`: string
- `knockemRevision`: string, short git commit hash
- `knockemRunmode`: string, production or testing
- `knockemVersion`: string, semantic version
- `maxCompetitionsActive`: int
- `maxCompetitionsFail`: int
- `submissionId`: string, submission UUID
- `status`: string
- `userEmail`: string, email

### `assays`
- `assayId`: string, assay UUID
- `competitionTimeoutSeconds`: int
- `containerEnv`: map of string to string
- `containerImage`: string, Docker Hub image name or a registry name
- `datetime`: string, ISO 8601
- `dependsOnAssayIds`: list of strings, assay UUIDs
- `genomeIdAlpha`: string
- `knockemRevision`: string, short git commit hash
- `knockemRunmode`: string, production or testing
- `knockemVersion`: string, semantic version
- `maxCompetitionsActive`: int
- `maxCompetitionsFail`: int
- `submissionId`: string, submission UUID
- `status`: string
- `userEmail`: string, email

### `competitions`
- `assayId`: string, assay UUID
- `containerEnv`: map of string to string
- `containerImage`: string, Docker Hub image name or a registry name
- `competitionId`: string, uuid
- `competitionTimeoutSeconds`: int
- `datetime`: string, ISO 8601
- `genomeIdAlpha`: string
- `genomeIdBeta`: string
- `knockemRevision`: string, short git commit hash
- `knockemRunmode`: string, production or testing
- `knockemVersion`: string, semantic version
- `knockoutSites`: string, space separated int
- `maxCompetitionsActive`: int
- `maxCompetitionsFail`: int
- `status`: string
- `submissionId`: string, submission UUID
- `userEmail`: string, email

### `dependencies`
- `dependencyId`: string, UUID
- `dependsOnId`: string, UUID
- `dependedById`: string, UUID
- `datetime`: string, ISO 8601
- `knockemRevision`: string, short git commit hash
- `knockemRunmode`: string, production or testing
- `knockemVersion`: string, semantic version
- `submissionId`: string, submission UUID

### atomic counters

for progress reports

- `submissionNumActiveCompetitions`
- `submissionNumFailedCompetitions`

maybe also in the future,
- `submissionNumCompletedCompetitions`
- `submissionNumPendingCompetitions`

## Assay Types enum

- `nulldist`
    - wt-wt competition
- `skeletonization`
    - strip down to a minimal set of genes with WT fitness
- `doseCalibration`
    - run a smear of dose level knockouts to calibrate titration dose selection
-`doseTitration`
    - run knockouts across a range of doses
