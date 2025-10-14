import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

import glob
import re



def extraer_numeros(lista_rutas, patron=r"T(\d+\.\d+)"):
    """
    Extrae números flotantes que siguen el patrón 'T' en una lista de cadenas.

    Args:
        lista_rutas (list): Lista de strings con rutas o nombres de archivo.
        patron (str): Expresión regular para capturar el número deseado.

    Returns:
        list: Lista de números extraídos como float.
    """
    numeros = []
    for ruta in lista_rutas:
        match = re.search(patron, ruta)
        if match:
            numeros.append(float(match.group(1)))
        else:
            print(f"⚠️ No se encontró número en: {ruta}")
    return numeros


# Buscar todos los archivos CSV en la carpeta
archivos = glob.glob("resultados/obs/observables_T*.csv")
# print(archivos)
# Leer y concatenar
df = pd.concat([pd.read_csv(f) for f in archivos], ignore_index=True)
# print(df)
# # Ordenar por temperatura
# df_total = df_total.sort_values(by="T")

# # Guardar archivo combinado
df.to_csv("observables_completo.csv", index=False)
print("Archivo combinado guardado como observables_completo.csv")


# Cargar datos
# df = pd.read_csv("observables_completo.csv")

# Estimar Tc (puede ajustarse)
Tc = 2.269

# Filtrar datos para T < Tc
df_sub = df[df[df.columns[0]] < Tc]
# print(df_sub)
T_vals = df_sub[df_sub.columns[0]].values
M_vals = np.abs(df_sub["M_prom"].values)  # Tomamos valor absoluto

# Modelo de ajuste


def modelo(T, beta, A):
    return A * (Tc - T)**beta


# Ajustar
params, cov = curve_fit(modelo, T_vals, M_vals)
beta_fit, A_fit = params

# Errores
beta_err = np.sqrt(cov[0][0])
print(f"β ajustado = {beta_fit:.4f} ± {beta_err:.4f}")


# Cargar datos
# df = pd.read_csv("observables_completo.csv")

# Estimar Tc (puede ajustarse)
# Tc = 2.269

# Crear carpeta de salida si querés
os.makedirs("graficos", exist_ok=True)
os.makedirs("graficos/ising", exist_ok=True)

dx = pd.to_numeric(df[df.columns[0]], errors='coerce')

# 1. Magnetización promedio vs T
plt.figure()
plt.plot(dx, df["M_prom"], marker='o', label="⟨M⟩")
plt.axvline(Tc, color='gray', linestyle='--', label=f"Tc ≈ {Tc}")
plt.xlabel("Temperatura T")
plt.ylabel("Magnetización ⟨M⟩")
plt.title("Magnetización promedio vs T")
plt.legend()
plt.grid()

plt.savefig("./graficos/grafico_M_vs_T.png")
plt.close()
# 2. Energía promedio vs T
plt.figure()
plt.plot(dx, df["E_prom"], marker='o', label="⟨E⟩", color='tab:red')
plt.xlabel("Temperatura T")
plt.axvline(Tc, color='gray', linestyle='--', label=f"Tc ≈ {Tc}")

plt.ylabel("Energía ⟨E⟩")
plt.title("Energía promedio vs T")
plt.grid()
plt.legend()

plt.savefig("./graficos/grafico_E_vs_T.png")
plt.close()
# 3. Calor específico vs T
plt.figure()
print(dx.dtypes)
print(df["cv"].dtypes)
plt.plot(dx, df["cv"], marker='o', label="cV", color='tab:green')
plt.axvline(Tc, color='gray', linestyle='--', label=f"Tc ≈ {Tc}")
plt.xlabel("Temperatura T")
plt.ylabel("Calor específico cV")
plt.title("Calor específico vs T")
plt.grid()
plt.legend()
plt.savefig("./graficos/grafico_cv_vs_T.png")
plt.close()

# 4. Susceptibilidad vs T
plt.figure()
plt.plot(dx, df["chi"], marker='o', label="χ", color='tab:purple')
plt.axvline(Tc, color='gray', linestyle='--', label=f"Tc ≈ {Tc}")
plt.xlabel("Temperatura T")
plt.ylabel("Susceptibilidad χ")
plt.title("Susceptibilidad vs T")
plt.grid()
plt.legend()
plt.savefig("./graficos/grafico_chi_vs_T.png")
plt.close()
# 5. Fracción aceptada vs T
plt.figure()
plt.plot(dx, df["aceptados"], marker='o',
         label="Fracción aceptada", color='tab:orange')
plt.axvline(Tc, color='gray', linestyle='--', label=f"Tc ≈ {Tc}")
plt.xlabel("Temperatura T")
plt.ylabel("Fracción de pasos aceptados")
plt.title("Fracción aceptada vs T")
plt.grid()
plt.legend()

plt.savefig("./graficos/grafico_aceptados_vs_T.png")
plt.close()
print("✅ Gráficos generados y guardados como PNG.")


# Cargar datos
# df = pd.read_csv("observables_completo.csv")

# Estimar Tc
Tc = 2.269

# Filtrar datos para T < Tc
df_sub = df[df[df.columns[0]] < Tc]
df_sup = df[df[df.columns[0]] > Tc]
T_vals = df_sub[df.columns[0]].values
T_valsP = df_sup[df.columns[0]].values
M_vals = np.abs(df_sub["M_prom"].values)  # valor absoluto
M_valsP = np.abs(df_sup["M_prom"].values)  # valor absoluto

# Transformar a log-log
x = np.log(Tc - T_vals)
y = np.log(M_vals)

# Transformar a log-log
xP = np.log(abs(Tc - T_valsP))
yP = np.log(M_valsP)
# print(Tc-T_valsP)
# print(Tc-T_valsP)
# Ajuste lineal: y = β * x + log(A)


def modelo_log(x, beta, logA):
    return beta * x + logA


params, _ = curve_fit(modelo_log, x, y)
beta_fit, logA_fit = params
A_fit = np.exp(logA_fit)

# Graficar
plt.figure(figsize=(8, 6))
plt.scatter(x, y, label="Datos simulados", color='tab:blue')
plt.plot(x, modelo_log(x, beta_fit, logA_fit),
         label=f"Ajuste: β = {beta_fit:.3f}", color='tab:red')
plt.xlabel("log(Tc − T)")
plt.ylabel("log(⟨M⟩)")
plt.title("Ajuste del exponente crítico β")
plt.legend()
plt.grid()
plt.savefig("./graficos/grafico_beta_loglog.png")
# plt.show()

print(f"✅ β ajustado = {beta_fit:.4f}")

params, _ = curve_fit(modelo_log, xP, yP)
beta_fit, logA_fit = params
A_fit = np.exp(logA_fit)

# Graficar
plt.figure(figsize=(8, 6))
plt.scatter(x, y, label="Datos simulados", color='tab:blue')
plt.plot(x, modelo_log(x, beta_fit, logA_fit),
         label=f"Ajuste: β = {beta_fit:.3f}", color='tab:red')
plt.xlabel("log(Tc − T)")
plt.ylabel("log(⟨M⟩)")
plt.title("Ajuste del exponente crítico β >Tc")
plt.legend()
plt.grid()
plt.savefig("./graficos/grafico_beta_loglog_TC.png")
# plt.show()

print(f"✅ β ajustado  T>Tc= {beta_fit:.4f}")


# Cargar la matriz
archivos = glob.glob("resultados/isingM/final_M_T*.csv")
# print(archivos)
temperaturas = extraer_numeros(archivos)

t = 0
j = 0
for i in archivos:
    estado = np.loadtxt(i)

    # Graficar como imagen
    plt.figure(figsize=(6, 6))
    plt.imshow(estado, cmap='gray', interpolation='nearest', origin='lower')
    plt.title(f"Estado final de la matriz de Ising T={temperaturas[t]}")
    plt.xlabel("j")
    plt.ylabel("i")
    plt.colorbar(label="Espín (+1 blanco, -1 negro)")
    plt.savefig(f"./graficos/ising/estado_final_ising_{temperaturas[t]}.png")
    # print(i,)
    plt.close()
    t += 1
    # plt.show()
