# !/bin/bash
pwd
ulimit -s unlimited  # Asigna una cantidad de memoria al proceso
echo "Compilando Dynamic"
# time muestra el tiempo que tarda en compilar un comando
mpirun -np 12 /usr/local/vasp.5.3/vasp # comando para compilar vasp
echo "Finalizado Dynamic"

