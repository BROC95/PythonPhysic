"""
Codigo para graficar PDOS
"""
import pandas as pd
import originpro as op

def is_string(x):
    return isinstance(x, str)

# Cargar el worksheet de Origin
ws = op.find_sheet()

#
#
## Convertir el worksheet a un DataFrame de Pandas
df = ws.to_df()
##print(df)
## Verificar las dos primeras columnas (ajustar 'col1' y 'col2' según el nombre de tus columnas)
col1 = df.iloc[:, 0]

is_string_series = col1.apply(is_string)
#print(is_string_series)
### Separar los datos donde hay NaN en las columnas
### Para la columna 1
split_col1 = col1[is_string_series].index.tolist()

k = 0
x = 0
df_list = [] 
for i in range(len(split_col1)):
    k=split_col1[i]
    d =df.iloc[x:k]
    print(x,k)
    d.columns = [col+str(i) for col in d.columns]
    df_list.append(d)
    x = k+1
    print("DATA",len(d))
    
kk = split_col1[-1]
pp = len(col1)
d =df.iloc[kk+1:pp]

df_list.append(d)


for i in range(len(df_list)):
    ##c =df_list[]
    #
    print(df_list[i].columns)
    #
##print(df_list[0])
dataN = []
for data in df_list:
    data.index = range(0, len(d))
    dataN.append(data)
    #
#
new_df = pd.concat([i for i in dataN],axis=1)
##new_df 

#
#
#
print(new_df)
#
print("Datos divididos y nuevas columnas creadas correctamente.")
wks = op.new_sheet()
wks.from_df(new_df)

