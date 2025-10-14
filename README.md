# 🧊 Simulación del Modelo de Ising 2D — Fortran + Python

Este proyecto implementa una simulación del modelo de Ising bidimensional utilizando Fortran para el núcleo computacional y Python para el análisis estadístico y visualización de resultados.

Se analizaron diferentes temperaturas deade 0.1 a 5 con un tamaño de paso de dT= 0.113, para una matriz de tamaño L = 30, la simulación se realizo con unidades reducidas con una semilla (seed) aleatoria, con un tamaño de paso de simulación  500000 y paso de termalización equivalente al 20%, los graficos respecto a la temperatura se analizaron entorno a la temperatura critica Tc = 2.269 .

---

## 📦 Estructura del Proyecto

```bash
ising2D/
├compile.sh                 # Código bash de automatización
│── ising.f90         # Módulo principal
│── makefile          # Automatización de compilación
├── graficos/              # Graficos  
│
├── resultados/           # Archivos CSV generados por simulación
│     
├── README.md             # Documentación del proyecto

```

---

## ⚙️ Requisitos

### Fortran
- Compilador compatible (e.g. `gfortran`)
- Makefile incluido para automatizar compilación

### Python
- Python ≥ 3.8
- Instalar dependencias:
```bash
pip install numpy 
pip install pandas
pip install scipy
```

---

## 🚀 Ejecución

### 1. Compilar y correr simulación
```bash
sh compile.sh
```

---

## 📊 Observables calculados

- Magnetización media ⟨M⟩
- Energía media ⟨E⟩
- Calor específico \( C_v \)
- Susceptibilidad magnética \(χ\)

Cada observable se calcula post-termalización y se guarda en archivos `.csv` para facilitar su análisis.

---

## 🧠 Visualización didáctica

Los scripts Python permiten:
- Graficar \( C_v \) vs temperatura
- Ajustar exponentes críticos
- Exportar figuras reproducibles para informes o clases

## 🤝 Contribuciones

Se agradecen mejoras en modularidad, visualización, documentación o integración con otros lenguajes. Abrí un issue o enviá un pull request.
