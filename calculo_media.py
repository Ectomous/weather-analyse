import pandas as pd
import os

# Define o caminho ao diretório que contém os arquivos de dados tratados e onde serão armazenados as médias e máximas.
filtered_data_dir = './db/filteredData/'
media_results_dir = './db/mediaResults/'

# Garante que o diretório de dados tratados existe.
os.makedirs(media_results_dir, exist_ok=True)

# Cria o laço de repetição para percorrer todos os arquivos tratatados para realizar o cáculo de médias e máximas.
for filename in os.listdir(filtered_data_dir):
    if filename.endswith('.csv'):
        # Constrói o caminho completo do arquivo.
        file_path = os.path.join(filtered_data_dir, filename)

        # Lê o arquivo .csv e carrega-o ao DataFrame.
        df = pd.read_csv(file_path)

        # Verifica e atribui a coluna de data correta.
        if 'DATA (YYYY-MM-DD)' in df.columns:
            df['DATA (YYYY-MM-DD)'] = pd.to_datetime(df['DATA (YYYY-MM-DD)'])
        elif 'Data' in df.columns:
            df['DATA (YYYY-MM-DD)'] = pd.to_datetime(df['Data'])
        else:
            raise KeyError("Nenhuma coluna de data encontrada no arquivo CSV.")

        # Extrai o mês e o ano
        df['Month'] = df['DATA (YYYY-MM-DD)'].dt.month
        df['Year'] = df['DATA (YYYY-MM-DD)'].dt.year

        # Calcula a média e a maior temperatura de cada mês
        monthly_avg = df.groupby('Month')['TEMPERATURA MÁXIMA NA HORA ANT. (AUT) (°C)'].mean()
        monthly_max = df.groupby('Month')['TEMPERATURA MÁXIMA NA HORA ANT. (AUT) (°C)'].max()

        # Calcula a média anual e a maior temperatura do ano
        annual_avg = df['TEMPERATURA MÁXIMA NA HORA ANT. (AUT) (°C)'].mean()
        annual_max = df['TEMPERATURA MÁXIMA NA HORA ANT. (AUT) (°C)'].max()

        # Salvar os resultados em arquivos separados para cada ano
        result_filename = os.path.join(media_results_dir, f'{filename[:-4]}.txt')
        with open(result_filename, 'w') as file:
            file.write("Médias mensais e maiores temperaturas de cada mês:\n")
            for month in range(1, 13):
                if month in monthly_avg.index:
                    file.write(f"Mês {month}: Média = {monthly_avg[month]:.2f}°C, Máxima = {monthly_max[month]:.2f}°C\n")
                else:
                    file.write(f"Mês {month}: Sem dados disponíveis\n")
            file.write(f"\nMédia anual: {annual_avg:.2f}°C\n")
            file.write(f"Maior temperatura do ano: {annual_max:.2f}°C\n")