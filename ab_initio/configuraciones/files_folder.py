"""
 Create folder by CI content


"""
import os
import shutil

#  Se modifica y crea un nuevo archivo VASP con la celda trasladada y nueva matriz


def readFile(file, t, name):
    with open(file, t) as fichero:
        lineas = fichero.readlines()
        lineas[0] = f"SYSTEM = {name}\n"
        fichero.seek(0)
        fichero.writelines(lineas)


pathBCi = os.getcwd()

# diCi solo debe contener los directorias a recorrer
dirCi = os.listdir()
# Extrae solo los datos que no sean ficheros
dirCi = [dire for dire in dirCi if not '.' in dire]
print(dirCi)
print(pathBCi)
os.chdir(dirCi[0])
srcD = os.getcwd()
CI = os.listdir()
# Extrae los nombres de las configuraciones
dirCi2 = [dire for dire in CI]
print(dirCi2)

os.chdir("..")
CIM = os.listdir()
vasp = CIM.index("VASP")

for i in dirCi2:
    dest = pathBCi+"/"+i
    srcCI = os.getcwd()+'/CI'
    src = os.getcwd()+'/'
    ori = src+'VASP/'
    #  Copia todo  de vasp creando una nueva carpeta, dest , ori (VASP)
    shutil.copytree(ori, dest, symlinks=False, ignore=None,
                    copy_function=shutil.copy2, ignore_dangling_symlinks=False)

    src = os.getcwd()
    destfile = src+'/'+i+'/static'
    destfileD = src+'/'+i+'/dynamic'
    file = src+'/CI/'+i
    #  Copia el archivo POSCAR en la configuracion en static
    shutil.copy(file, destfile)
    new_path = f"{destfile}/POSCAR"
    shutil.move(file, new_path)
    INCARS = destfile+'/INCAR'
    INCARD = destfileD + "/INCAR"
    print(INCARD)
    name = i
    readFile(INCARS, 'r+', name+" St")
    readFile(INCARD, 'r+', name+" Dy")
