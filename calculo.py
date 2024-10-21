import pandas as pd

df = pd.read_csv('./db/filteredData/2024.csv')

media_temperatura = df['TEMPERATURA MÁXIMA NA HORA ANT. (AUT) (°C)'].mean()

print(f"A média das temperaturas filtradas é: {media_temperatura:.2f}°C")
