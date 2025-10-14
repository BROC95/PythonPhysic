import sys

# Leer el primer argumento (temperatura)
if len(sys.argv) < 2:
    print("Uso: python3 graph.py <temperatura>")
    sys.exit(1)

T = sys.argv[1]
print(f"Temperatura recibida: {T}")

import pandas as pd
import matplotlib.pyplot as plt


archivo = f"resultados/terma/TermaU_T{T}.csv"
print(archivo)
termaU = pd.read_csv(archivo)
hist_E = pd.read_csv(f"resultados/histE/hist_E_T{T}.csv")
hist_M = pd.read_csv(f"resultados/histM/hist_M_T{T}.csv")
# Leer datos
# data = pd.read_csv("termaliza.csv")

# Crear figura con dos subplots
fig, axs = plt.subplots(2, 1, figsize=(10, 8), sharex=True)
data = termaU
# Subplot 1: Energía promedio
axs[0].plot(data[data.columns[0]], data[data.columns[1]], color='tab:red', label="Energía promedio")
axs[0].set_ylabel("Energía ⟨E⟩")
axs[0].set_title(f"Termalización del modelo de Ising T = {T}")
axs[0].legend()
axs[0].grid(True)

# Subplot 2: Magnetización promedio
axs[1].plot(data[data.columns[0]], data[data.columns[2]], color='tab:blue', label="Magnetización promedio")
axs[1].set_xlabel("Paso Monte Carlo")
axs[1].set_ylabel("Magnetización ⟨M⟩")
axs[1].legend()
axs[1].grid(True)

# Guardar figura
plt.tight_layout()
plt.savefig(f"./resultados/Termalizacion_{T}.png")
# plt.show()

# Tc_index = np.argmax(np.gradient(data[data.columns[2]]))
# Tc_estimada = data["T"][Tc_index]
# data = pd.read_csv("observables.csv")

# plt.figure(figsize=(10, 6))
# plt.plot(data["T"], data["M_prom"], label="⟨M⟩", marker='o')
# plt.plot(data["T"], data["E_prom"], label="⟨E⟩", marker='s')
# plt.plot(data["T"], data["aceptados"], label="Fracción aceptada", marker='^')
# plt.xlabel("Temperatura T")
# plt.ylabel("Observables")
# plt.legend()
# plt.grid()
# plt.title("Observables vs Temperatura")
# plt.savefig("Observables_vs_T.png")



import numpy as np

E = hist_E
# M = np.loadtxt("hist_M_T2.00.csv")
M = hist_M

fig, axs = plt.subplots(1, 2, figsize=(12, 5))
axs[0].hist(E, bins=50, color='tab:red')
axs[0].set_title(f"Histograma de Energía (T={T})")
axs[1].hist(M, bins=50, color='tab:blue')
axs[1].set_title(f"Histograma de Magnetización (T={T})")
plt.savefig(f"./resultados/Histogramas_{T}.png")


Tc = 2.269
# T_vals = data["T"][data["T"] < Tc]
# M_vals = data["M_prom"][data["T"] < Tc]

# from scipy.optimize import curve_fit

# def modelo(T, beta):
#     return (Tc - T)**beta

# params, _ = curve_fit(modelo, T_vals, M_vals)
# print("Exponente crítico β =", params[0])