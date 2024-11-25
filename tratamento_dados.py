import pandas as pd
import os

# Define o caminho ao diretório que contém os arquivos de dados brutos e onde serão armazenados os dados tratados.
raw_data_dir = './db/rawData/'
filtered_data_dir = './db/filteredData/'

# Certifica que o diretório de dados tratados existe.
os.makedirs(filtered_data_dir, exist_ok=True)

# Cria o laço de repetição para percorrer todos os arquivos no diretório de dados brutos
for filename in os.listdir(raw_data_dir):
    if filename.endswith('.csv'):
        # Constrói o caminho completo do arquivo.
        file_path = os.path.join(raw_data_dir, filename)

        # Carrega o arquivo CSV com tabulação como delimitador e pula as primeiras 8 linhas, que possuem informações sobre a cidade, desnecessárias para o projeto.
        df = pd.read_csv(file_path, encoding='ISO-8859-1', sep='\t', skiprows=8)

        # Renomeia as colunas para padronizar seus nomes, visto que, com o passar dos anos, a base de dados CSV mudou o nome das colunas.
        df.columns = ['DATA (YYYY-MM-DD)', 'Hora UTC', 'TEMPERATURA MÁXIMA NA HORA ANT. (AUT) (°C)']

        # Verifica e converte a coluna de temperatura máxima para o tipo 'number', visto que em um dos arquivos CSV o valor de temperatura foi passado como 'string'.
        if df['TEMPERATURA MÁXIMA NA HORA ANT. (AUT) (°C)'].dtype == 'object':
            df['TEMPERATURA MÁXIMA NA HORA ANT. (AUT) (°C)'] = df['TEMPERATURA MÁXIMA NA HORA ANT. (AUT) (°C)'].str.replace(',', '.').astype(float)

        # Remove as linhas onde a coluna de temperatura máxima está vazia ou igual a -9999.
        df_limpado = df.dropna(subset=['TEMPERATURA MÁXIMA NA HORA ANT. (AUT) (°C)'])
        df_limpado = df_limpado[df_limpado['TEMPERATURA MÁXIMA NA HORA ANT. (AUT) (°C)'] != -9999].copy()

        # Verifica o formato da coluna de horário e converte adequadamente
        try:
            df_limpado['Hora UTC'] = pd.to_datetime(df_limpado['Hora UTC'].str.replace(' UTC', ''), format='%H%M').dt.time
        except ValueError:
            df_limpado['Hora UTC'] = pd.to_datetime(df_limpado['Hora UTC'].str.replace(' UTC', ''), format='%H:%M').dt.time

        # Filtra os horários entre 08:00h e 18:00h
        df_filtrado = df_limpado[df_limpado['Hora UTC'].between(pd.to_datetime('08:00').time(), pd.to_datetime('18:00').time())]

        # Salva o DataFrame filtrado em um novo arquivo CSV no diretório de dados filtrados
        filtered_file_path = os.path.join(filtered_data_dir, filename)
        df_filtrado.to_csv(filtered_file_path, index=False)