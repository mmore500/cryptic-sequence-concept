## Update Loop

### Assay Kickoff Handler
- check for pending assays with completed dependencies
- generate knockout variants with container command and add to noSQL
    - mark ephemeral
- generate competition requests into REDIS/noSQL
    - add first competition attempt to REDIS pending competition attempts

### Assay Completion Handler
- check for active assays with no competions in active competitions
- retrieve completed competitionResults form noSQL
- generate assayResults into noSQL
- remove assay from active assays

### Competition Attempt Kickoff Handler
- check for pending competition attempts
- for all with submission active competition attempts is less than max active
    - increment submission active attempts
    - use shell command to launch competition attempt with container
    - ACID:
        - remove from pending attempts REDIS
        - add to active competition attempts REDIS

### Competition Attempt Completion Handler
- for all active competitions, check whether result is in nosql database
- if result is present,
    - remove from active competition attempts REDIS
    - decrement submission active attempts

### Competition Timeout Handler
- check for active competition attempts with timeout seconds plus datetime greater than now
- if fail count is less than max fail,
    - generate new UUID and move from active to pending, update active competitions
- increment submission fail count
- decrement submission active attempts

### Max Fail Handler
-  for all REDIS databases, check whether submissionId has fail count greater than max fail and if so delete entry

### Submission Completion Handler
- for all active submissions, check whether no assays are in `pendingAssays`
or `activeAssays`; if so, remove from active submissions and delete entries in atomic counters

## Submission Endpoint
- add to active submissions REDIS
- add to pending assays REDIS

- record submission in database
- record assays in database
