

import sys
import os
import numpy as np


#  quitamos espacios
def datN(info):
    try:
        for i in range(3):
            index = info.index("")
            info.pop(index)
        return info
    except:
        return info

#  Extraemos los archivos con la extension determinada
def identExt(path,ext):
    contenido = os.listdir(path)
    # print("conte:")
    # logging.info(contenido)
    # print(contenido)
    data = []
    for fichero in contenido:
        if os.path.isfile(os.path.join(path, fichero)) and fichero.endswith(ext):
            data.append(fichero)
    return data

# def filevasp(Data,linea):
#     Data.append(linea.replace("\n"," TTT\n"))
#     return Data


# def readFile(file,t):
#     i =0
#     Data2 = []
#     with open(file, t) as fichero:
#         linea = fichero.readline()
#         # linea2 = fichero.readlines()
#         # print(linea2)
#         # print("**"*100)
#         Data = []
#         Mat = []
#         identity ="""1.0  0.0  0.0
#         0.0  1.0  0.0
#         0.0  0.0  1.0
#             """

#         k=0
#         while linea != '':

#             # print(i,linea, end='')
#             # print(linea)
#             linea = fichero.readline()
#             i+=1
            
#             if i>-1 and i<5:
#                 k+=1
#                 # print(k,linea.split(" "),end="")
#                 Mat.append(linea.replace("\n",""))
#             else:
#                 Data.append(linea)
     
        
#         mat = ['20.0  0.0  0.0', '0.0  20.0  0.0', '0.0  0.0  20.0']

#         mat = mat[::-1]
#         mat.append(Mat[0])
#         mat = mat[::-1]
#         # print(mat)
        

#     # Data = Data[5:-3]
#     # n = len(Data)
#     # Data =Data[::-1]
#     # Data = Data.append("\n")
#     # n = n-1
#     # Data = Data.append(n)
#     # Data = Data[::-1]
#     # print(Data)
    
#     with open(file+"_file", "a") as fichero:
#         fichero.write(file+":\n")
#         for k in mat:
#             fichero.write(k+"\n")
#         for line in Data:
#             fichero.write(line)


#  Se modifica y crea un nuevo archivo VASP con la celda trasladada y nueva matriz
def readFile(file,t):
    i =0
    Data2 = []
    with open(file, t) as fichero:
        linea = fichero.readline()
        # linea2 = fichero.readlines()
        # print(linea2)
        # print("**"*100)
        Data = []
        Mat = []
        identity ="""30.0  0.0  0.0\n0.0  30.0  0.0\n0.0  0.0  30.0\n"""

        k=0
        Mat.append(linea)
        while linea != '':

            print(i,linea, end='')
          
            # print(linea)
            linea = fichero.readline()
            if i>=0 and i<7:
#                 k+=1
                #  print(k,linea.split(" "),end="")
                # print(linea)
                if i<1 or i>=4:
                    Mat.append(linea)
                if i==3:
                    Mat.append(identity)
                
                # Mat.append(linea.replace("\n",""))

            #  Se modifica las lineas dependiendo de los espacios entre columnas  x y z
            else:
                # print( "     " in linea)
                if  "     " in linea:
                    linea=linea.replace("     "," ")
                if  "    " in linea:
                    linea=linea.replace("    ","     ")
                    linea=linea.replace("     ","")
                

                Data.append(linea.replace("\n",""))
            i+=1
    print("DATA")
    # print(Data)

    #  Se elimina componentes vacias
    Data.pop()
    # print(Data)

    DataCenter = []



    # print(Data)
    
    #  Se modifica la matriz de coordenadas  transformando el archivo a matriz  tipo numpy 
    
    for linea in Data:
        info = linea.split(" ")
        # print(linea)
        linea = datN(info)
        vect =[float(dat) for dat in linea]

        ve = (np.array(vect))

        #  Operacion de traslación operando en la matriz

        ve =ve-4+15
        ve = np.array2string(ve)
        ve = ve[1:-1]
        DataCenter.append(ve)
    #     # print("____")
        # d = np.array2string(ve)

        # print(ve[0])
        # print("nn")
    # for k in DataCenter:
    #     print(k)

    name = file.split('.VASP')
    name = name[0]
    #  Se crea un nuevo archivo de salida con la modificación 

    with open(name+"_CELDA.VASP", "a") as fichero:
       
        for k in Mat:
             fichero.write(k)
        for k in DataCenter:
            
            fichero.write(str(k)+"\n")
  
        

if __name__ == "__main__":
    
    #  Se extraen todos los archivos con extension .VASP
    files  = identExt('./',".VASP")
    print(files)
    print(len(files))
    
    #  Se modifica cada uno de los archivos .VASP
    
    for k in range(len(files)):
    # k=0
        readFile(file=files[k],t='r')
    # # readFile(file=files[0],t='r')

    # files  = identExt('./',".txt")
    # print(files)
    # print(len(files))
    
