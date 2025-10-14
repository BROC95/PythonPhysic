#!/bin/bash

clear
make

Tmin=0.1
Tmax=5.0
Tstep=0.113

mkdir -p resultados/obs/
mkdir -p resultados/terma/
mkdir -p resultados/histE/
mkdir -p resultados/histM/
mkdir -p resultados/isingM/

for T in $(seq $Tmin $Tstep $Tmax); do
    echo "Simulación para T = $T"
    date '+ %Y-%m-%d  %H:%M:%S'

    ./ising_p1 "$T"
    mv observables.csv "resultados/obs/observables_T${T}.csv"
    mv Terma_U.csv "resultados/terma/TermaU_T${T}.csv"
    mv hist_E.csv "resultados/histE/hist_E_T${T}.csv"
    mv hist_M.csv "resultados/histM/hist_M_T${T}.csv"
    mv estado_final.csv "resultados/isingM/final_M_T${T}.csv"
    python3 ./graph.py ${T}
done

python3 ./dataObs.py 