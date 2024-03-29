#!/bin/bash
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
