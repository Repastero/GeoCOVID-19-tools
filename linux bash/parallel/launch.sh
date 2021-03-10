#!/bin/bash
#SBATCH --job-name=PNA_00
#SBATCH --ntasks=10

INSTANCES=2 # instancias paralelas por cpu
SCENARIO_FOLDER=scenario.rs
PARAM_FILE=unrolledParamFile.txt

OUTPUT_CSV=`date +"%d-%m-%Y-%H-%M"`.csv
START=`date +%s`

cd parana # directorio modelo
for (( i=1; i<=$INSTANCES; i++ ))
do
    echo "Iniciando $SLURM_NTASKS instancias de $((INSTANCES * SLURM_NTASKS))"
    srun java -Xmn512m -cp './lib/*' repast.simphony.batch.InstanceRunner \
        -pxml ./$SCENARIO_FOLDER/batch_params.xml \
        -scenario ./$SCENARIO_FOLDER \
        -id $i \
        -pinput $PARAM_FILE &
    sleep 5
done
wait

echo "Uniendo archivos de Reportes"
rm ./*batch_param_map*.csv
awk 'FNR==1 && NR!=1{next;}{print}' ./Reporte*.csv >> "../$OUTPUT_CSV"
rm ./Reporte*.csv

echo "Duracion total $((($(date +%s)-$START)/60)) minutos"
