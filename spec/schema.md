## noSQL database

for job report-back and data storage

### `genomes`
- `content`: string
- `datetime`: string, ISO 8601
- `id`: string, RFC 4122 UUID
- `numSites`: int
- `revisionKnockem`: string, short git commit hash
- `userEmail`: string, email

### `submissions`
- `assayIds`: list of strings, assay UUIDs
- `assayTypes`: list of strings (enum)
- `containerImage`: string, Docker Hub image name or a registry name
- `datetime`: string, ISO 8601
- `genomeId`: string
- `id`: string, RFC 4122 UUID
- `maxActive`: int
- `maxFail`: int
- `revisionKnockem`: string, short git commit hash
- `userEmail`: string, email

Inconsistencies/Notes:
- The `shell` requirement is not listed within the attributes but is mentioned as required in the user submission.

### `assays`
- `assayType`: string (enum)
- `competitionIDs`: list of strings, competition UUIDs
- `datetime`: string, ISO 8601
- `id`: string, RFC 4122 UUID
- `revisionKnockem`: string, short git commit hash
- `submissionId`: string, submission UUID
- `userEmail`: string, email

### `assayResults`
- `datetime`: string, ISO 8601
- `id`: string, RFC 4122 UUID (corresponding to entry in `assays`)
- `result`: string, JSON
- `revisionKnockem`: string, short git commit hash

### `competitions`
- `assayId`: string, assay UUID
- `datetime`: string, ISO 8601
- `id`: string, RFC 4122 UUID
- `knockoutSites`: list of int
- `revisionKnockem`: string, short git commit hash
- `submissionId`: string, submission UUID
- `userEmail`: string, email

### `competitionResults`
- `assayId`: string, assay UUID
- `competitionAttemptId`: string, RFC 4122 UUID
- `datetime`: string, ISO 8601
- `id`: string, RFC 4122 UUID (corresponding to entry in `competitions`)
- `result`: string, JSON
- `revisionKnockem`: string, short git commit hash
- `submissionId`: string, submission UUID
- `userEmail`: string, email

### `competitionAttempts`
- `assayId`: string, assay UUID (listed twice, might be an inconsistency)
- `datetime`: string, ISO 8601
- `id`: string, RFC 4122 UUID (corresponding to entry in `competitions`)
- `knockoutSites`: list of int
- `revisionKnockem`: string, short git commit hash
- `submissionId`: string, submission UUID
- `userEmail`: string, email

### `competitionAttemptResults`
- `assayId`: string, assay UUID
- `competitionId`: string, competition UUID
- `datetime`: string, ISO 8601
- `id`: string, RFC 4122 UUID (corresponding to entry in `competitionResults`)
- `revisionKnockem`: string, short git commit hash
- `result`: string, JSON
- `submissionId`: string, submission UUID
- `userEmail`: string, email

## redis database

for server job orchestration

### `activeSubmissions`
- `assayIds`: list of strings, assay UUIDs
- `datetime`: string, ISO 8601
- `genomeId`: string
- `id`: string, RFC 4122 UUID
- `revisionKnockem`: string, short git commit hash
- `submissionId`: string, submission UUID
- `userEmail`: string, email

### `pendingAssays`
- `assayId`: string, assay UUID
- `datetime`: string, ISO 8601
- `dependsOnAssayIds`: list of strings, assay UUIDs
- `genomeId`: string
- `id`: string, RFC 4122 UUID
- `revisionKnockem`: string, short git commit hash
- `submissionId`: string, submission UUID
- `userEmail`: string, email

### `activeAssays`
- `assayId`: string, assay UUID
- `datetime`: string, ISO 8601
- `dependsOnCompetitionIds`: list of strings, competition UUID
- `genomeId`: string
- `id`: string, RFC 4122 UUID
- `revisionKnockem`: string, short git commit hash
- `submissionId`: string, submission UUID
- `userEmail`: string, email

### `activeCompetitions`
- `assayId`: string, assay UUID
- `datetime`: string, ISO 8601
- `dependsOnCompetitionAttemptId`: string, competition attempt UUID
- `genomeId`: string
- `id`: string, RFC 4122 UUID
- `knockoutSites`: list of int
- `revisionKnockem`: string, short git commit hash
- `submissionId`: string, submission UUID
- `userEmail`: string, email

### `pendingCompetitionAttempts`
- `assayId`: string, assay UUID
- `datetime`: string, ISO 8601
- `genomeId`: string
- `id`: string, RFC 4122 UUID
- `knockoutSites`: list of int
- `revisionKnockem`: string, short git commit hash
- `submissionId`: string, submission UUID
- `timeoutSeconds`: int
- `userEmail`: string, email

### `activeCompetitionAttempts`
- `assayId`: string, assay UUID
- `datetime`: string, ISO 8601
- `genomeId`: string
- `id`: string, RFC 4122 UUID
- `knockoutSites`: list of int
- `revisionKnockem`: string, short git commit hash
- `submissionId`: string, submission UUID
- `timeoutSeconds`: int
- `userEmail`: string, email

### atomic counters

for progress reports

- `submissionNumPendingAssays`
- `submissionNumActiveAssays`
- `submissionNumCompletedAssays`
- `submissionNumPendingCompetitions`
- `submissionNumActiveCompetitions`
- `submissionNumCompletedCompetitions`

## Assay Types enum

- `nulldist`
    - wt-wt competition
- `skeletonization`
    - strip down to a minimal set of genes with WT fitness
- `doseCalibration`
    - run a smear of dose level knockouts to calibrate titration dose selection
-`doseTitration`
    - run knockouts across a range of doses
