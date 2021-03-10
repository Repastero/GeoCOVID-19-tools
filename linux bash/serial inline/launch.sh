#!/bin/bash
#SBATCH --job-name=PNA_00
#SBATCH --ntasks=20

SCENARIO_FOLDER=scenario.rs
PARAM_FILE=unrolledParamFile.txt

OUTPUT_CSV=`date +"%d-%m-%Y-%H-%M"`.csv
START=`date +%s`

cd parana # directorio modelo
for (( i=1; i<=$SLURM_NTASKS; i++ ))
do
    echo "Iniciando $i task de $SLURM_NTASKS"
	srun --ntasks=1 java -Xmn512m -cp './lib/*' repast.simphony.batch.InstanceRunner \
        -pxml ./$SCENARIO_FOLDER/batch_params.xml \
        -scenario ./$SCENARIO_FOLDER \
        -id $i \
'1	cantidadMuertosLimite	400,corridas	1,diaEntradaCaso	0,diasSimulacion	244,diasMinimoSimulacion	244,nombreMunicipio	parana,diaInicioSimulacion	182,cantidadInfectados	1
2	cantidadMuertosLimite	400,corridas	1,diaEntradaCaso	0,diasSimulacion	244,diasMinimoSimulacion	244,nombreMunicipio	parana,diaInicioSimulacion	182,cantidadInfectados	1
3	cantidadMuertosLimite	400,corridas	1,diaEntradaCaso	0,diasSimulacion	244,diasMinimoSimulacion	244,nombreMunicipio	parana,diaInicioSimulacion	182,cantidadInfectados	1
4	cantidadMuertosLimite	400,corridas	1,diaEntradaCaso	0,diasSimulacion	244,diasMinimoSimulacion	244,nombreMunicipio	parana,diaInicioSimulacion	182,cantidadInfectados	1' &
    sleep 2
done
wait

echo "Uniendo archivos de Reportes"
rm ./*batch_param_map*.csv
awk 'FNR==1 && NR!=1{next;}{print}' ./Reporte*.csv >> "../$OUTPUT_CSV"
rm ./Reporte*.csv

echo "Duracion total $((($(date +%s)-$START)/60)) minutos"
