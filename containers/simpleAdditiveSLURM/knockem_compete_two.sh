#!/bin/bash

if [ -z "${SLURM_JOB_ID}" ]; then
    echo "non-SLURM environment detected, forwarding to SLURM job & exiting"

    python3 -m knockem.cli forward-to-slurm knockem_compete_two <<EOF
#!/bin/bash -login
########## Define Resources Needed with SBATCH Lines ##########
#SBATCH --time=4:00:00               # Time limit hrs:min:sec
#SBATCH --job-name knockem_${KNOCKEM_COMPETITION_ID}
#SBATCH --account=devolab
#SBATCH --output="/mnt/home/%u/joblog/id=%j+ext.txt"
#SBATCH --mem=4G
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --mail-type=FAIL
# No --mail-user, the default value is the submitting user
#SBATCH --exclude=csn-002,amr-250
# Job may be requeued after node failure.
#SBATCH --requeue

# -----------------------------------------------------------------------------
echo "log context..."
# -----------------------------------------------------------------------------
echo "date \$(date)"
echo "hostname \$(hostname)"
echo "job \${SLURM_JOB_ID:-none}"
echo "user \${USER}"
echo "KNOCKEM_SUBMISSION_ID=${KNOCKEM_SUBMISSION_ID}"
echo "KNOCKEM_COMPETITION_ID=${KNOCKEM_COMPETITION_ID}"

# -----------------------------------------------------------------------------
echo "set up matthew's idiosyncratic SLURM creature comforts..."
# -----------------------------------------------------------------------------
ln -s "\${HOME}/scratch" "/mnt/scratch/\${USER}/" || :
mkdir -p "\${HOME}/joblog" || :

if [[ -z \${SLURM_JOB_ID:-} ]]; then
  export JOBLOG_PATH="/dev/null"
else
  export JOBLOG_PATH="\$(ls "\${HOME}/joblog/"*"id=\${SLURM_JOB_ID}+"*)"
fi
echo "JOBLOG_PATH \${JOBLOG_PATH}"

mkdir -p "\${HOME}/joblatest" || :
ln -srfT "\${JOBLOG_PATH}" "\${HOME}/joblatest/start" || :

export JOBSCRIPT_PATH="\$0"
echo "JOBSCRIPT_PATH \${JOBSCRIPT_PATH}"
readlink -f "\${JOBSCRIPT_PATH}"
export JOBSCRIPT_PATH="\$(readlink -f "\${JOBSCRIPT_PATH}")"
echo "JOBSCRIPT_PATH \${JOBSCRIPT_PATH}"

mkdir -p "\${HOME}/jobscript" || :
cp "\${JOBSCRIPT_PATH}" "\${HOME}/jobscript/id=\${SLURM_JOB_ID:-none}+stage=\${STAGE}+ext=.slurm.sh" || :

# -----------------------------------------------------------------------------
echo "do work..."
# -----------------------------------------------------------------------------
temp_dir="\$(mktemp -d)"
pwd

echo {{{knockem_run_command}}}
{{{knockem_run_command}}}
echo "date \$(date)"
echo "SECONDS \${SECONDS}"
EOF
    exit 0
else
    echo "SLURM environment detected, proceeding..."
fi

# Fetch genomes
genome_alpha=$(python3 -m knockem.cli fetch-genome "$KNOCKEM_GENOME_ID_ALPHA")
genome_beta=$(python3 -m knockem.cli fetch-genome "$KNOCKEM_GENOME_ID_BETA")

echo "Genome alpha: $genome_alpha"
echo "Genome beta: $genome_beta"

# Run competition (example: summing genome values)
sum_alpha=$(echo "$genome_alpha" | awk '{sum+=$1} END {print sum}')
sum_beta=$(echo "$genome_beta" | awk '{sum+=$1} END {print sum}')

echo "Sum alpha: $sum_alpha"
echo "Sum beta: $sum_beta"

# Logic to determine numalpha and numbeta would go here
updatesElapsed=100
numAlpha="$(awk "BEGIN {print 1000 * $sum_alpha / ($sum_alpha + $sum_beta)}")"
numBeta="$(awk "BEGIN {print 1000 * $sum_beta / ($sum_alpha + $sum_beta)}")"

echo "Updates elapsed: $updatesElapsed"
echo "Num alpha: $numAlpha"
echo "Num beta: $numBeta"

# Report competition results
python3 -m knockem.cli report-competition "${updatesElapsed}" "${numAlpha}" "${numBeta}"
python3 -m knockem.cli cleanup-genome "$KNOCKEM_GENOME_ID_ALPHA"
python3 -m knockem.cli cleanup-genome "$KNOCKEM_GENOME_ID_BETA"
