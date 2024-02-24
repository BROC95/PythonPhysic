import os
import shutil
import subprocess




def compileFileSh():
    process = subprocess.call(['sh','./compilarVasp.sh'])








# diCi solo debe contener los directorias a recorrer
dirCi = os.listdir()
# Extrae solo los datos que no sean ficheros
dirCi = (dire for dire in dirCi if not '.' in dire) # Generator 
pathBCi = os.getcwd()


for ci in dirCi:
    # os.chdir(pathBCi)
   
    pathCi = pathBCi+'/'+ci  # Crea el path de cada CI
    # print(pathCi)
    os.chdir(pathCi) # Cambia al directorio CI
    
    pathB = os.getcwd()
    dirL = os.listdir() # Lista la informacion en CI
    # print(pathB)
    #  Crea los paths static y dynamic
    static = dirL[dirL.index('static')]
    pathStatic = pathB+'/'+static
    dynamic = dirL[dirL.index('dynamic')]
    pathDynamic = pathB+'/'+dynamic
    print("Completed! Paths")





    if static:
        # Si la carpeta static existe, cambia al directorio y compila el archivo bash
        print("Estatico")
        os.chdir(pathStatic)
        # print(os.getcwd())
        # print("ANTES BASH")
        compileFileSh()
        # print("END BASH")
        dirSt = os.listdir()
        # print(dirSt)
        # POSCAR = dirSt[dirSt.index('POSCAR')]

        #  Copia el archivo POSCAR en la el destino
        src = pathStatic+'/POSCAR'
        # print(src)
        # print("POSCAR")
        des = pathDynamic
        shutil.copy2(src, des)
        
    if dynamic:
        print("Dinamico")
        dirDy = os.listdir()
        # print(dirDy)
        os.chdir(pathDynamic)
        dirDy = os.listdir()
        # print(dirDy)
        # print(os.getcwd())
        compileFileSh()
        # dirDy = os.listdir()
        # print(dirDy)
        # print("________________")
        # print(os.getcwd())

    print("END CI")

