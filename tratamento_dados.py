import pandas as pd

# Carregar o arquivo CSV com tabulação como delimitador e pulando as primeiras 8 linhas
df = pd.read_csv('./db/rawData/2024.csv', encoding='ISO-8859-1', sep='\t', skiprows=8)

# Mostrar as primeiras linhas para verificar a leitura correta
# print(df.head())

# Renomear as colunas para remover caracteres especiais
df.columns = ['Data', 'Hora UTC', 'TEMPERATURA MÁXIMA NA HORA ANT. (AUT) (°C)']

# Verificar e renomear a coluna de data, se necessário
if 'DATA (YYYY-MM-DD)' in df.columns:
    df.rename(columns={'DATA (YYYY-MM-DD)': 'DATA (YYYY-MM-DD)'}, inplace=True)
elif 'Data' in df.columns:
    df.rename(columns={'Data': 'DATA (YYYY-MM-DD)'}, inplace=True)
else:
    raise KeyError("Nenhuma coluna de data encontrada no arquivo CSV.")

# Remover as linhas onde a coluna de temperatura é igual a -9999
df_limpado = df[df['TEMPERATURA MÁXIMA NA HORA ANT. (AUT) (°C)'] != -9999].copy()  # Use .copy() para evitar o aviso

# Converter a coluna de data para garantir que está no formato de data
df_limpado['DATA (YYYY-MM-DD)'] = pd.to_datetime(df_limpado['DATA (YYYY-MM-DD)'], errors='coerce')

# Verificar o formato da coluna de horário e converter adequadamente
try:
    df_limpado['Hora UTC'] = pd.to_datetime(df_limpado['Hora UTC'].str.replace(' UTC', ''), format='%H%M').dt.time
except ValueError:
    df_limpado['Hora UTC'] = pd.to_datetime(df_limpado['Hora UTC'].str.replace(' UTC', ''), format='%H:%M').dt.time

# Filtrar os horários entre 08:00h e 18:00h
df_filtrado = df_limpado[df_limpado['Hora UTC'].between(pd.to_datetime('08:00').time(), pd.to_datetime('18:00').time())]

# Salvar o DataFrame filtrado em um novo arquivo CSV
df_filtrado.to_csv('./db/filteredData/2024.csv', index=False)

# Conferir as primeiras linhas após a remoção e filtragem de horário
# print(df_filtrado.head())