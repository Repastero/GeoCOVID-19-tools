# Descripción
- parallel: para iniciar las instancias al mismo tiempo (por la cantidad de tasks).
- repast 2.8: los que trae Repast a partir de esta version para SLURM (sin testear). 
- repast default: los que trae Repast, pero modificados para funcionar en SLURM.
- serial inline: igual a "serial" pero pasando los parametros en texto plano, no archivo.
- serial (**recomendado**): inicia una instancia por tasks, por la cantidad de nodos (separadas por un delay).
