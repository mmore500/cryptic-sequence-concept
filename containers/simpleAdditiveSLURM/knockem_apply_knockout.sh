#!/bin/bash
# Read genome content from stdin
genome=$(cat /dev/stdin)

# Apply knockout to specified sites
for site in "$@"
do
    genome=$(echo "$genome" | awk -v site="$site" 'NR==site{$1="0"}1')
done

# Output the knocked out genome
echo "$genome"
