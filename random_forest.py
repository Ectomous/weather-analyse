# Importação de bibliotecas necessárias para a análise
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
import matplotlib.pyplot as plt

# Variável contendo os anos analisados.
dados_anos = np.array([2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024])
# Variável contendo as temperaturas médias.
medias_anuais = np.array([27.99, 27.99, 28.50, 28.31, 28.05, 28.29, 28.9, 29.45, 28.63, 28.20, 28.18, 28.12, 29.46, 28.61, 28.26, 27.70, 27.84, 28.11, 27.76, 29.05, 29.05, 28.45])
# Variável contendo as temperaturas máximas.
maximas_anuais = np.array([36.10, 36.20, 36.80, 35.80, 35.30, 35.50, 36.30, 35.80, 35.50, 36.50, 34.60, 36.10, 37.60, 37.10, 37.40, 36.10, 35.20, 35.70, 34.20, 35.50, 36.90, 35.40])

# Criação do DataFrame com lag features (temperaturas dos anos anteriores)
data = pd.DataFrame({'Ano': dados_anos, 'Media': medias_anuais, 'Maxima': maximas_anuais})
data['Media_lag1'] = data['Media'].shift(1)
data['Media_lag2'] = data['Media'].shift(2)
data['Maxima_lag1'] = data['Maxima'].shift(1)
data['Maxima_lag2'] = data['Maxima'].shift(2)

# Remover as linhas iniciais com valores nulos
data.dropna(inplace=True)

# Dividir dados em X (features) e y (targets)
X = data[['Ano', 'Media_lag1', 'Media_lag2', 'Maxima_lag1', 'Maxima_lag2']]
y_media = data['Media']
y_maxima = data['Maxima']

# Treinar o modelo Random Forest Regressor para médias
modelo_rf_media = RandomForestRegressor(n_estimators=100, random_state=0)
modelo_rf_media.fit(X, y_media)

# Treinar o modelo Random Forest Regressor para máximas
modelo_rf_maxima = RandomForestRegressor(n_estimators=100, random_state=0)
modelo_rf_maxima.fit(X, y_maxima)

# Prever para os próximos anos usando previsão iterativa
anos_futuros = np.arange(2025, 2041)
previsoes_media = []
previsoes_maxima = []

# Usar as últimas duas médias e máximas conhecidas para iniciar a previsão
media_lag1 = medias_anuais[-1]  # Último valor de temperatura média conhecido
media_lag2 = medias_anuais[-2]  # Penúltimo valor de temperatura média conhecido
maxima_lag1 = maximas_anuais[-1]  # Último valor de temperatura máxima conhecido
maxima_lag2 = maximas_anuais[-2]  # Penúltimo valor de temperatura máxima conhecido

for ano in anos_futuros:
    # Criar a entrada como um DataFrame com nomes de colunas
    X_futuro = pd.DataFrame([[ano, media_lag1, media_lag2, maxima_lag1, maxima_lag2]], columns=['Ano', 'Media_lag1', 'Media_lag2', 'Maxima_lag1', 'Maxima_lag2'])
    
    # Fazer a previsão para médias
    pred_media = modelo_rf_media.predict(X_futuro)[0]
    previsoes_media.append(pred_media)
    
    # Fazer a previsão para máximas
    pred_maxima = modelo_rf_maxima.predict(X_futuro)[0]
    previsoes_maxima.append(pred_maxima)
    
    # Atualizar os lags para o próximo ano
    media_lag2 = media_lag1
    media_lag1 = pred_media
    maxima_lag2 = maxima_lag1
    maxima_lag1 = pred_maxima

# Exibir as previsões
for ano, previsao_media, previsao_maxima in zip(anos_futuros, previsoes_media, previsoes_maxima):
    print(f"Ano {ano}: Previsão de média de temperatura = {previsao_media:.2f}°C, Previsão de temperatura máxima = {previsao_maxima:.2f}°C")

# Plotar a série histórica e as previsões
plt.figure(figsize=(12, 6))

plt.subplot(2, 1, 1)
plt.plot(dados_anos, medias_anuais, label='Médias Anuais Históricas', color='blue')
plt.plot(anos_futuros, previsoes_media, label='Previsão Random Forest (Média)', color='green', linestyle='--')
plt.xlabel('Ano')
plt.ylabel('Média Anual de Temperatura (°C)')
plt.legend()
plt.title('Previsão de Temperatura Média Anual com Random Forest')

plt.subplot(2, 1, 2)
plt.plot(dados_anos, maximas_anuais, label='Máximas Anuais Históricas', color='red')
plt.plot(anos_futuros, previsoes_maxima, label='Previsão Random Forest (Máxima)', color='orange', linestyle='--')
plt.xlabel('Ano')
plt.ylabel('Máxima Anual de Temperatura (°C)')
plt.legend()
plt.title('Previsão de Temperatura Máxima Anual com Random Forest')

plt.tight_layout()
plt.show()
