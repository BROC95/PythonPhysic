#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 29 11:55:37 2020

@author: breyneroc
"""


# Permitividad en un sistema RC
import numpy as np
import os,sys
import matplotlib.pyplot as plt
from matplotlib import rc
import time




print(sys.version)
print(os.getcwd())

print(sys.api_version)
#  Datos del sistema

# Funciones
def Zr(w):
    return R/(1+(w*R*C)**2)
def Zi(w):
    return (w*C*R**2)/(1+(w*R*C)**2)



# Variables de condiciones iniciales
Wn = 5
Wi = 0
Wk =1000000
R=4
C=100
wtao=1/(R*C)
print(wtao)
s=np.linspace(Wi,Wn,Wk) ## Frecuencias 
lw=np.log10(s)
#0 a 50Mhz
N=len(s)
file=open("DataZ.txt","w")
DatosZr=[]
DatosZi=[]


# Agregar datos evaluados en la función 
DatosZr.append(Zr(s))
DatosZi.append(Zi(s))



file.write('Zr=%s'%DatosZr+ '\n')
file.write('Zi=%s'%DatosZi+ '\n')


file.close()

#Crea archivos txt de los datos función file


        


plt.rc('text', usetex=True)
plt.rc('font', family='serif')


plt.figure(figsize=(6, 4))

plt.subplot(2, 2, 1)

plt.plot(Zr(s), Zi(s) ,'g.-')
plt.title("$Z\' vs Z\"$")
plt.xlabel(r"$Zr$")
plt.ylabel(r"$Zi$")


plt.subplot(2, 2, 2)

plt.plot(lw, Zi(s) ,'b.-',label="Zi")
plt.plot( lw,Zr(s) ,'r.-',label=r"Z")

plt.title("$log(\omega) vs Z' Z\"$")
plt.xlabel(r"$log(\omega)$")
plt.ylabel(r"$Zi,Zr$")


plt.subplot(2, 2, 3)
plt.title("$log(\omega) vs Z\"$")
plt.xlabel(r"$log(\omega)$")
plt.ylabel(r"$Zi$")

plt.plot( lw,Zi(s) ,'b.-',label=r"Z")


plt.subplot(2, 2, 4)

plt.plot(lw,Zr(s) ,'r.-',label=r"Z")
plt.title("$log(\omega) vs Z\'$")
plt.xlabel(r"$log(\omega)$")
plt.ylabel(r"$Zr$")

plt.tight_layout()




#plt.savefig("SimulimpedanciaZrZinyq")







plt.show()

print("Maximo en Zi(wtao)=",Zi(wtao)," con Zr(wtao)=",Zr(wtao))

print(N)


for i in range(N):
    if (round(Zr(s[i]))==2):
        print(lw[i])
   


