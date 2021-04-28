#!/bin/bash
#SBATCH --job-name=err_24		# create a short name for your job
#SBATCH --nodes=1				# node count
#SBATCH --ntasks-per-node=24	# total number of tasks per node
#SBATCH --cpus-per-task=1		# cpu-cores per task (>1 if multi-threaded tasks)

SCENARIO_FOLDER=scenario.rs
PARAM_FILE=unrolledParamFile.txt
START=`date +%s`

# Para calcular el numero de instancias = nodes * ntasks-per-node
# El numero de corridas = instancias * lineas en PARAM_FILE
cd entrerios # carpeta modelo
for (( i=1; i<=$SLURM_NTASKS_PER_NODE; i++ )) do
	echo "Iniciando $i task de $SLURM_NTASKS_PER_NODE"
	srun --ntasks=$SLURM_NNODES java -Xmn512m -cp './lib/*' repast.simphony.batch.InstanceRunner \
		-pxml ./$SCENARIO_FOLDER/batch_params.xml \
		-scenario ./$SCENARIO_FOLDER \
		-id $i \
		-pinput $PARAM_FILE &
	sleep 2
	: '
	Si srun falla por id de usuario invalida,
	se puede correr igual pero en un solo nodo (--nodes=1)
	correr comando sin la parte de srun: "java -Xmn512m ...".
	'
done
wait

echo "Uniendo archivos de Reportes"
rm ./*batch_param_map*.csv
awk 'FNR==1 && NR!=1{next;}{print}' ./Reporte*.csv >> "../${SLURM_JOB_ID}.csv"
rm ./Reporte*.csv

echo "Duracion total $((($(date +%s)-$START)/60)) minutos"
