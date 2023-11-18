


import os

from ase.io.vasp import write_vasp
from ase.io import read


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
    print(files)
    print(len(files))
    for file in files:
        centerVASP(file)
    

    