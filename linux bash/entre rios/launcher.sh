#!/bin/bash
#SBATCH --job-name=ENTRE_24
#SBATCH --ntasks=24

SCENARIO_FOLDER=scenario.rs
PARAM_FILE=unrolledParamFile.txt
INSTANCES=1 # instancias paralelas por cpu

OUTPUT_CSV=`date +"%d-%m-%Y-%H-%M"`.csv
START=`date +%s`

SCENARIO_FOLDERS=(pna gchu concord)
SCENARIO_NAMES=(parana gualeguaychu concordia)

for (( sc=0; sc<"${#SCENARIO_NAMES[*]}"; sc++ )) do
	cur_scenario=${SCENARIO_NAMES[$sc]}
	cd ${SCENARIO_FOLDERS[$sc]}
	echo "Iniciando scenario $cur_scenario"
	for (( i=1; i<=$INSTANCES; i++ )) do
		echo "Iniciando instancia $i en $SLURM_NTASKS tasks"
		for (( j=1; j<=$SLURM_NTASKS; j++ )) do
			echo "Task $j de $SLURM_NTASKS"
			srun --ntasks=1 java -Xmn512m -cp './lib/*' repast.simphony.batch.InstanceRunner \
				-pxml ./$SCENARIO_FOLDER/batch_params.xml \
				-scenario ./$SCENARIO_FOLDER \
				-id $i$j \
				-pinput $PARAM_FILE &
		   sleep 2
		done
	done
	wait
	echo "Uniendo archivos de scenario $cur_scenario"
	# borra el primer param y elimina el resto
	i=0
	for filename in ./*batch_param_map*.csv; do 
		if [[ $i -eq 0 ]] ; then 
			mv "$filename" "../${cur_scenario}_param_${SLURM_JOB_ID}.csv"
			i=$(( $i + 1 ))
		else
			rm $filename
		fi
	done
	#
	awk 'FNR==1 && NR!=1{next;}{print}' ./Reporte*.csv >> "../${cur_scenario}_${SLURM_JOB_ID}.csv"
	rm ./Reporte*.csv
	cd ..
done

# genera grafica unicamente si corrio los 3 escenarios
if [[ $sc -eq 3 ]] ; then 
	echo "Creando grafica de camas"
	source ~/python3-ve/bin/activate
	python graph_er.py $SLURM_JOB_ID
	deactivate
fi
#

echo "Duracion total $((($(date +%s)-$START)/60)) minutos"
