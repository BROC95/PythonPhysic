#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 28 16:54:23 2020

@author: breyneroc
"""

#  Codigo modificado de
# https://tecnologiainformaticadeep.blogspot.com/2020/05/algortitmo-genetico-en-python-simple.html

# Comienza el codigo

import random
import numpy as np
import matplotlib.pyplot as plt 
import time
start = time.perf_counter()
individuos = 200
cromosomas = 3**5
generaciones = 1000

Fitness={'PU':10,'V':-1,'C':-5}
#Creando un arreglo de 5 x 6
poblacion = [[0 for x in range(cromosomas)] for x in range(individuos)]

#print("POBLACION INICIAL")
# mapa=np.array([[0, 0, 1, 1],
#                 [1, 1, 1, 0],
#                 [0, 0, 0, 0],
#                 [1, 1, 0, 1]])

#Llenando la población aleatoriamente
for individuo in range(individuos):
    for cromosoma in range(cromosomas):
        poblacion[individuo][cromosoma] = random.randint(0, 6)

# Crea el mundod de robby
mapa=np.random.randint(0,2,(10,10))
#Función para medir aptitud
def medir_aptitud(poblacion):
    aptitud = [0 for i in range(individuos)]
    fitness={'PU':10,'V':-1,'C':-5}
    #valores = ["Signo", 1, 5, 10]
    # print("")
    # print("VALORES PARA DETERMIANR APTITUD MUSICAL")
    # print(valores)
    # print(aptitud)
    # print(fitness)
    #x,y=np.shape(mapa)
    #print(x,y)
    
    # Multiplicndo el Vector de Aptitud por el cromosoma ( fila) de cada individuo de la Poblacion.
    datc=[]
    dat=[]
    
    """
action (0 = MoveNorth, 1 = MoveSouth, 2 =
MoveEast, 3 = MoveWest, 4 = StayPut, 5 = PickUp, and 6 =
RandomMove)
Estados posibles 
Pareda lata vació
"""
    #poblacion=[4,4,4,4,5]
    #poblacion=[[3, 3, 4, 3, 3]]
    x=0
    y=0
    k=0
    j=0
    # s=sum(mapa)
    # s=sum(s)
    limx=len(mapa)
    # puntosM=s*fitness['PU']
    # print("Puntos maximos",puntosM)
    # print("Punto de partida en el mapa",x,y)
    for individuo in range(individuos):
        for cromosoma in range(cromosomas):
                #print(mapa[x][y])
                #print(k,j)
            
                
                if poblacion[individuo][cromosoma]==0:
                    # Desplaza hacia arriba una posición
                    k=x
                    x=x-1
                    if x<0:
                        #print("Pared")
                        aptitud[individuo] += fitness['C']
                        x=k
                    else:
                        p=0
                        #print(mapa[x][y])
                    
                    #print(x,y)
                    # if x>=limx:
                    #     mapa[x][y]=mapa[limx][y]
                    #     k=k-1
                    #     print(mapa[x][y])
                    #continue
                if poblacion[individuo][cromosoma]==1:
                    # Desplaza hacia abajo una posición
                    k=x
                    x=x+1
                    if x<limx:
                        #print(mapa[x][y])
                        p=0
                        
                    else:
                        #print("Pared")
                        aptitud[individuo] += fitness['C']
                        x=k
                        
                    
                    #print(1)
                    #continue
                if poblacion[individuo][cromosoma]==2:
                    # Desplaza hacia arriba una posición
                    j=y
                    y=y+1
                    if y<limx:
                        p=0
                        #print(mapa[x][y])
                        
                    else:
                        #print("Pared")
                        aptitud[individuo] += fitness['C']
                        y=j
                
                    
                    #print(2)
                    #continue
                if poblacion[individuo][cromosoma]==3:
                    # Desplaza hacia izquierda una posición
                    j=y
                    y=y-1
                    if y<0:
                        #print("Pared")
                        aptitud[individuo] += fitness['C']
                        y=j
                    else:
                        p=0
                        #print(mapa[x][y])
                   
                    #print(3)
                    #continue
                if poblacion[individuo][cromosoma]==4:
                    # Desplaza hacia arriba una posición
                    k=x
                    j=y
                    #print(mapa[x][y])
        
                    #print(4)
                    #continue
                if poblacion[individuo][cromosoma]==5:
                    #print(5)
                    if mapa[x][y]==1:
                        aptitud[individuo] += fitness['PU']
                        #mapa[x][y]=0
                        #continue
                    else:
                        aptitud[individuo] += fitness['V']
                        #continue
                if poblacion[individuo][cromosoma]==6:
                    poblacion[individuo][cromosoma]=np.random.randint(0,6)
  

    #Imprimiendo valores de aptitud de cada  fila o cromosoma
#     print("")
#     print("APTITUD")
#     for individuo in range(individuos):
#         print(str(individuo) + " - [" + ", ".join(str(f) for f in poblacion[individuo]) + "] = " + "{:}".format(aptitud[individuo]))
        
 
# # Imprimiendo la Aptitud Total de la Poblacion ( Sumas de las Aptitudes de sus individuos)
#     total_aptitud = 0
#     for x in range(individuos):
#         total_aptitud += abs(aptitud[x])
#     print("TOTAL APTITUD " + str(total_aptitud))
#     print("")
    aptitud=np.array(aptitud)
    return aptitud

s=sum(mapa)
s=sum(s)

puntosM=s*Fitness['PU']
print("Puntos maximos",puntosM)

def maxfit(dat):
    n=len(dat)
    datmax=[]
    datind=[]
    for i in range(n):
        ind = np.unravel_index(np.argmax(dat, axis=None), dat.shape)
        datind.append(ind)
        datmax.append(np.max(dat))
        dat=np.delete(dat,ind)
        if i>=1:
            break
    datind=[i[0] for i in datind]
    return datind,datmax




def cruce(indice_individuos):
    
    # print("CRUCE")
    # print(str(indice_individuos[0]) + " - [" + ", ".join(str(f) for f in poblacion[indice_individuos[0]]) + "]")
    # print(str(indice_individuos[1]) + " - [" + ", ".join(str(f) for f in poblacion[indice_individuos[1]]) + "]")
    
    #indice_cruce = random.randint(1, cromosomas - 1)
    indice_cruce = int(len(poblacion[0])/2)
    #print("Índice de cruce " + str(indice_cruce));
    #print("Descendencias")
    descendencia1 = poblacion[indice_individuos[0]][:indice_cruce] + poblacion[indice_individuos[1]][indice_cruce:]
    #print(descendencia1)
    descendencia2 = poblacion[indice_individuos[1]][:indice_cruce] + poblacion[indice_individuos[0]][indice_cruce:]
    #print(descendencia2)
    return descendencia1, descendencia2



# def imprime_poblacion():
#     for individuo in range(individuos):
#         print(str(individuo) + " - [" + ", ".join(str(f) for f in poblacion[individuo]) + "]")


#
#
aptitud=[]
Fitmax=[]
ngen=[]
for gen in range(generaciones):
    ngen.append(gen)
    # print(poblacion)
    # print("")
    indice_hijos = individuos // 2
    fitness=medir_aptitud(poblacion)
    pos,fitmax=maxfit(fitness)
    fitgenm=max(fitmax)
    Fitmax.append(fitgenm)
    des1,des2=cruce(pos)
    for k in range(0, individuos // 2, 2):
        poblacion[indice_hijos],poblacion[indice_hijos + 1] = cruce(pos)
        indice_hijos += 1
    poblacion=poblacion
    #poblacion=np.array([[1, 2, 2, 5, 4, 1],
                        # [4, 5, 3, 0, 0, 1],
                        # [0, 2, 4, 5, 3, 5],
                        # [4, 3, 1, 4, 5, 2],
                        # [3, 1, 0, 3, 3, 3]])
        
        
        #poblacion = [[0 for x in range(cromosomas)] for x in range(individuos)]
    #     print("")
    #poblacion = nueva_generacion
    #print(i)
# for generacion in range(generaciones):
#     print("")
#     print("--------- GENERACIÓN " + str(generacion) +" ---------")
#     #imprime_poblacion()
#     n=medir_aptitud(poblacion)
#     nueva_generacion = [0 for x in range(individuos)]
 
    
  

    # for i in range(individuos // 2):
    #     individuo_ganador = torneo(i, individuos - 1 -i)
    #     nueva_generacion[i] = poblacion[individuo_ganador]

    # mutaciones = random.randint(0, individuos // 2)
    # for j in range(mutaciones):
    #     mutacion(random.randint(0, mutaciones))

    # indice_hijos = individuos // 2
    # for k in range(0, individuos // 2, 2):
    #     nueva_generacion[indice_hijos], nueva_generacion[indice_hijos + 1] = cruce(k, k+1)
    #     indice_hijos += 2
    #     print("")

    #poblacion = nueva_generacion

print("")
print("------- ÚLTIMA GENERACIÓN -------")
#imprime_poblacion()
#medir_aptitud(poblacion)
print("Punto min",min(Fitmax))
print("Punto max",max(Fitmax))
seconds = time.perf_counter() - start

print('Time op {:.2f} seconds.'.format(seconds))
start = time.perf_counter()
plt.plot(ngen,Fitmax )
#plt.ylim(0,puntosM)
#plt.xlim(0,generaciones)
plt.xlabel("Generacion")
plt.ylabel("fitness")
plt.title("Robby")
plt.grid()
plt.savefig("FitRobby1.png")
plt.show()
seconds = time.perf_counter() - start

print('Time gra {:.2f} seconds.'.format(seconds))
