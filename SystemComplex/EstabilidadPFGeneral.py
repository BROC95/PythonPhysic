# -*- coding: utf-8 -*-
"""
Created on Thu Apr 22 18:03:17 2021

@author: ASUS
"""
import matplotlib.pyplot as plt
import numpy as np

Dom= 10
n=2
N=100

M=[]
Mdet=[]
Mtrac=[]
for i in range(N):
    matriz =np.around( np.random.uniform(-Dom,Dom,size=(n,n)),n)
    eigenvalue, featurevector =np.linalg.eig(matriz)
    #print(eigenvalue)
    det= np.around(np.linalg.det(matriz),2)
    trac= np.around(np.trace(matriz),2)
    Mdet.append(det)
    Mtrac.append(trac)
    M.append(eigenvalue)
    

L=np.max(Mdet)
P=np.max(Mtrac)
x= np.arange(0,L)
Mr=np.real(M)
Mi=np.imag(M)

Mdet=np.array(Mdet)
Mtrac=np.array(Mtrac)
text=f'N={N}'
plt.title(f"Clasificación General \nP.Fijos ")
plt.axhline(y=0, color="black", linestyle=":")
plt.axvline(x=0, color="black", linestyle=":")

plt.annotate(text, xy=(0,0), xytext=(-L, -P),fontsize=15)
raizp=np.sqrt(4*x)

plt.plot(raizp,'r',label=r"$\tau=\sqrt{4\Delta}$")
plt.plot(-raizp,color='orange',label=r"$\tau=-\sqrt{4\Delta}$")
colors=(Mtrac+Mdet)/2
# scatter(theta, r, c=colors, s=area, cmap='hsv', alpha=0.75)

plt.scatter(Mdet,Mtrac,c=colors,cmap='viridis', alpha=0.75)
plt.xlabel(r"$\Delta$")
plt.ylabel(r"$\tau$")
plt.legend()
plt.show()


r=0
m=0
silla=0
Nines=0
Nest=0
centro=0
star=0
Eines=0
Eest=0
igual=0
posx=[]
posy=[]
negx=[]
negy=[]

def rp(det):
    f=np.sqrt(4*det)
    return f
for i in range(N):
    if Mdet[i]<0:
        silla+=1
        # Puntos silla
    if Mdet[i]>0 and Mtrac[i]>0:
       
        posy.append(Mtrac[i])
        posx.append(Mdet[i])
        r+=1
        
    if Mdet[i]>0 and Mtrac[i]<0:
        negx.append(Mdet[i])
        negy.append(Mtrac[i])
        m+=1
    if Mdet[i]>0 and Mtrac[i]==0:
        centro+=1
        #centros
    if Mdet[i] == 0:
        star+=1
        

Np=len(posy)
for i in range(Np):
    
    if posy[i]>rp(posx[i]):
        Nines+=1
     
        # Nodos inestables


    if posy[i] <rp(posx[i]):
        Eines+=1
    if posy[i] ==rp(posx[i]):
        igual+=1
        print(igual)
    
        #espirales inestables
        
Nn=len(negy)
for i in range(Nn):
    
    if negy[i]>-rp(negx[i]):
        Eest+=1

        # Espirales estables

    if negy[i] <-rp(negx[i]):
        Nest+=1
      
        # Nodos estables


Nt =silla+star+centro+Eest+Eines+Nest+Nines



Psilla= round(silla/N*100,2)
Pstar= round(star/N*100,2)
PCentro= round(centro/N*100,2)
PEspStab= round(Eest/N*100,2)
PEspIStab= round(Eines/N*100,2)
PNodStab= round(Nest/N*100,2)
PNodIStab= round(Nines/N*100,2)

Npor=Psilla+Pstar+PNodIStab+PEspStab+PEspIStab+PNodStab
print("\nPorcentaje P.Silla\n",Psilla)
print("Porcentaje P.Nodo estable\n",PNodStab)
print("Porcentaje P.Espiral Estable\n",PEspStab)
print("Porcentaje P.Nodo Inestable\n",PNodIStab)
print("Porcentaje P.Espiral Inestable\n",PEspIStab)
print("Porcentaje P.Estrella\n",Pstar)
print("Porcentaje P.Centro\n",PCentro)


print("Suma porce",Npor)

