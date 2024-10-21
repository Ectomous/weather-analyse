import pandas as pd

# Ler o arquivo CSV
df = pd.read_csv('./db/filteredData/2024.csv')

# Verificar e atribuir a coluna de data correta
if 'DATA (YYYY-MM-DD)' in df.columns:
    df['DATA (YYYY-MM-DD)'] = pd.to_datetime(df['DATA (YYYY-MM-DD)'])
elif 'Data' in df.columns:
    df['DATA (YYYY-MM-DD)'] = pd.to_datetime(df['Data'])
else:
    raise KeyError("Nenhuma coluna de data encontrada no arquivo CSV.")

# Extrair o mês e o ano
df['Month'] = df['DATA (YYYY-MM-DD)'].dt.month
df['Year'] = df['DATA (YYYY-MM-DD)'].dt.year

# Calcular a média e a maior temperatura de cada mês
monthly_avg = df.groupby('Month')['TEMPERATURA MÁXIMA NA HORA ANT. (AUT) (°C)'].mean()
monthly_max = df.groupby('Month')['TEMPERATURA MÁXIMA NA HORA ANT. (AUT) (°C)'].max()

# Calcular a média anual e a maior temperatura do ano
annual_avg = df['TEMPERATURA MÁXIMA NA HORA ANT. (AUT) (°C)'].mean()
annual_max = df['TEMPERATURA MÁXIMA NA HORA ANT. (AUT) (°C)'].max()

# Exibir os resultados
print("Médias mensais e maiores temperaturas de cada mês:")
for month in range(1, 13):
    if month in monthly_avg.index:
        print(f"Mês {month}: Média = {monthly_avg[month]:.2f}°C, Maior = {monthly_max[month]:.2f}°C")
    else:
        print(f"Mês {month}: Sem dados disponíveis")

print(f"\nMédia anual: {annual_avg:.2f}°C")
print(f"Maior temperatura do ano: {annual_max:.2f}°C")

# Escrever os resultados em um arquivo de texto
with open('./db/mediaResults/2024.txt', 'w') as file:
    file.write("Médias mensais e maiores temperaturas de cada mês:\n")
    for month in range(1, 13):
        if month in monthly_avg.index:
            file.write(f"Mês {month}: Média = {monthly_avg[month]:.2f}°C, Maior = {monthly_max[month]:.2f}°C\n")
        else:
            file.write(f"Mês {month}: Sem dados disponíveis\n")
    file.write(f"\nMédia anual: {annual_avg:.2f}°C\n")
    file.write(f"Maior temperatura do ano: {annual_max:.2f}°C\n")