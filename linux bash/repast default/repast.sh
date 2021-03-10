#!/bin/bash
#SBATCH --job-name=SEC2_00
#SBATCH --ntasks=4

cd $SLURM_SUBMIT_DIR

# number of parameter combinations per job
run_per_instance=4

# lines in unrolled batch file
f=unrolledParamFile.txt
lines=`wc -l $f | cut -f1 -d' '`
echo "Total lines: $lines"

# while total_full_instances > 0
np=$SLURM_NTASKS
echo "Total processing cpus: $np"

let "remaining_instances = ($lines + $run_per_instance - 1) /  $run_per_instance"

count=0
while (( $remaining_instances > 0 ))
do
    if [ "$remaining_instances" -lt "$np" ]
        then
        np=$remaining_instances
    fi
    srun $SLURM_SUBMIT_DIR/repastwrapper.sh $lines $run_per_instance $count $f
    count=$(( $count + $np ))
    let remaining_instances=$remaining_instances-$np
done
echo "Completed all runs."
