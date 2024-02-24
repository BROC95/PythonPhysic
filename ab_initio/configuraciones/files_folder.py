"""
 Create folder by CI content


"""
import os
import shutil



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
    src= os.getcwd()+'/'
    ori = src+'VASP/'
    #  Copia todo  de vasp creando una nueva carpeta, dest , ori (VASP)
    shutil.copytree(ori, dest, symlinks=False, ignore=None, copy_function=shutil.copy2, ignore_dangling_symlinks=False)

    src =os.getcwd()
    destfile = src+'/'+i+'/static'
    file = src+'/CI/'+i
    #  Copia el archivo POSCAR en la configuracion en static
    shutil.copy(file, destfile)