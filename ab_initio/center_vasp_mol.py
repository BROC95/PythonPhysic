import sys
import os

import numpy as np

from ase.io.vasp import write_vasp
from ase.io import read



#  Se modifica y crea un nuevo archivo VASP con la celda trasladada y nueva matriz
def readFile(file,t,cu):
    i =0
    Data = []
    Mat = []
    with open(file, t) as fichero:
        linea = fichero.readline()
       
       
        In =f"""{cu}.0  0.0  0.0\n0.0  {cu}.0  0.0\n0.0  0.0  {cu}.0\n"""
        k=0
        Mat.append(linea)
        while linea != '':

            # print(i,linea, end='')
          
            # print(linea)
            linea = fichero.readline()
            if i>=0 and i<7:
#                 k+=1
                #  print(k,linea.split(" "),end="")
                # print(linea)
                if i<1 or i>=4:
                    Mat.append(linea)
                if i==3:
                    # Mat.append(identity)

                    Mat.append(In)
                
                # Mat.append(linea.replace("\n",""))

            #  Se modifica las lineas dependiendo de los espacios entre columnas  x y z
            else:
                

                Data.append(linea)
            i+=1
    # print("DATA")
    # print(Data)

    #  Se elimina componentes vacias
    Data.pop()
    # print(Data)

    DataCenter = []


    with open(file, "w") as fichero:
        
        # print("matrix")
        for k in Mat:
            #  print(k)
             fichero.write(k)
        for k in Data:
            
            fichero.write(k)
    # print(file)
        


#  Centra los datos usando la libreria ase
def centerVASP(file):
    atoms = read(file)
    name = file.split('.VASP')
    atoms.center()
    name_output= name[0]+"_CU"+str(atoms.get_cell()[0][0])+'_.VASP'
    write_vasp(name_output, atoms)


#  Extraemos los archivos con la extension determinada
def identExt(path,ext):
    contenido = os.listdir(path)
    data = []
    for fichero in contenido:
        if os.path.isfile(os.path.join(path, fichero)) and fichero.endswith(ext):
            data.append(fichero)
    return data



if __name__ == "__main__":
    
       #  Se extraen todos los archivos con extension .VASP
    files  = identExt('./',".VASP")
    # print(files)
    # print(len(files))
    cu=30
    for file in files:
        readFile(file=file,t='r',cu=cu)
        centerVASP(file)
    

    
