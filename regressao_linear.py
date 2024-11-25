# Importação de bibliotecas necessárias para a análise
import numpy as np
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt

# Variável contendo os anos analisados.
dados_anos = np.array([2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024]).reshape(-1, 1)
# Variável contendo as temperaturas médias.
medias_anuais = np.array([27.99, 27.99, 28.50, 28.31, 28.05, 28.29, 28.9, 29.45, 28.63, 28.20, 28.18, 28.12, 29.46, 28.61, 28.26, 27.70, 27.84, 28.11, 27.76, 29.05, 29.05, 28.45])
# Variável contendo as temperaturas máximas.
maximas_anuais = np.array([36.10, 36.20, 36.80, 35.80, 35.30, 35.50, 36.30, 35.80, 35.50, 36.50, 34.60, 36.10, 37.60, 37.10, 37.40, 36.10, 35.20, 35.70, 34.20, 35.50, 36.90, 35.40])

# Criação do modelo de regressão linear para médias anuais
modelo_medias = LinearRegression()
modelo_medias.fit(dados_anos, medias_anuais)

# Criação o modelo de regressão linear para máximas anuais
modelo_maximas = LinearRegression()
modelo_maximas.fit(dados_anos, maximas_anuais)

# Previsão das temperaturas médias/máximas do ano 2025 a 2040
anos_futuros = np.array([2025, 2026, 2027, 2028, 2029, 2030, 2031, 2032, 2033, 2034, 2035, 2036, 2037, 2038, 2039, 2040]).reshape(-1, 1)
previsoes_medias = modelo_medias.predict(anos_futuros)
previsoes_maximas = modelo_maximas.predict(anos_futuros)

# Exibição no terminal das previsões
for ano, previsao_media, previsao_maxima in zip(anos_futuros.flatten(), previsoes_medias, previsoes_maximas):
    print(f"Ano {ano}: Previsão de média de temperatura = {previsao_media:.2f}°C, Previsão de máxima de temperatura = {previsao_maxima:.2f}°C")

# Plot dos dados e previsões
plt.scatter(dados_anos, medias_anuais, color='blue', label='Médias Anuais Históricas')
plt.plot(anos_futuros, previsoes_medias, color='red', linestyle='--', label='Previsão de Médias')
plt.scatter(dados_anos, maximas_anuais, color='green', label='Máximas Anuais Históricas')
plt.plot(anos_futuros, previsoes_maximas, color='orange', linestyle='--', label='Previsão de Máximas')
plt.xlabel('Ano')
plt.ylabel('Temperatura (°C)')
plt.legend()
plt.show()
