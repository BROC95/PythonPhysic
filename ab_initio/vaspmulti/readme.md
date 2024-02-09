# Compilar archivos vasp 

Programa que compila archivos vasp estatico y dinamico 

# Bash

En un archivo bash, que se encuentra en cada carpeta con los datos vasp, se definen los comandos normales de compilación por terminal, luego se le dan permisos de ejecución y escritura.


```bash
chmod +x archivo.sh
```
# Carpetas
La estruCtura de carpetas por configuración, debe contener una carpeta estatica y dinamica, 

## static
La carpeta  debe tener los siguientes archivos en el directorio: INCAR, KPOINTS, POTCAR, POSCAR

## dynamic
La carpeta  debe tener los siguientes archivos en el directorio: INCAR, KPOINTS, POTCAR

Nota: En ambas carpetas debe estar el archivo con extensión .sh , ya que es el encargado de ejecutar los comandos de vasp

# Compilación

Para ejecutar el programa, se debe tener las carpetas por configuración de interacción, con las respectivas carpetas de estatico y dinamico, con el archivo bash, luego se recorre cada carpeta, y se ejecuta el comando bash para ejecutar el programa vasp e iniciar el cálculo.

```bash
python3 script.py  
```
