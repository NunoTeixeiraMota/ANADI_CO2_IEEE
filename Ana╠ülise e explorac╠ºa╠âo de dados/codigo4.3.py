import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Carregar os dados de emissões de CO2
caminho_dados_co2 = 'CO_data.csv'
co_data = pd.read_csv(caminho_dados_co2)



# Filtrar os dados para o período de 2000 a 2021
co_data_filtered = co_data[(co_data['year'] >= 2000) & (co_data['year'] <= 2021)]

# Agrupar os dados por região e ano, somando as emissões de CO2 do carvão
co_data_grouped = co_data_filtered.groupby(['country', 'year'])['coal_co2'].sum().reset_index()

# Filtrar os dados para incluir apenas as regiões especificadas
regions = ['Africa', 'Asia', 'South America', 'North America', 'Europe', 'Oceania']
co_data_regions = co_data_grouped[co_data_grouped['country'].isin(regions)]

# Pivotar os dados para ter anos como linhas e regiões como colunas
co_data_pivot = co_data_regions.pivot(index='year', columns='country', values='coal_co2')

# Calcular a tabela de correlação entre as regiões
correlation_matrix = co_data_pivot.corr()

correlation_matrix


# Gerar um gráfico da matriz de correlação usando seaborn
plt.figure(figsize=(10, 8))
sns.heatmap(correlation_matrix, annot=True, cmap="coolwarm", fmt=".2f")
plt.show()

#%%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import statsmodels.api as sm
from statsmodels.stats.outliers_influence import variance_inflation_factor
from scipy.stats import linregress


# Filtrar os dados para os anos pares do século XXI
years_even = [year for year in range(2000, 2022, 2)]
co2_data_filtered = co_data[(co_data['year'].isin(years_even))]

# Definir os países para as variáveis independentes e a região para a variável dependente
countries_vars = ['Germany', 'Russia', 'France', 'Portugal']
dependent_region = 'Europe'

# Criar a tabela de dados para as variáveis independentes e dependentes
pivot_data = co2_data_filtered.pivot_table(index='year', columns='country', values='coal_co2')
X = pivot_data[countries_vars].dropna()
Y = pivot_data[dependent_region].dropna().reindex(X.index)  # Garantir alinhamento dos índices entre X e Y

# Adicionar a constante ao modelo
X_const = sm.add_constant(X)

# Construir o modelo de regressão linear
model = sm.OLS(Y, X_const).fit()

# Análise dos resíduos - Gráfico de Resíduos vs Valores Ajustados em plot separado
plt.figure(figsize=(6, 5))
plt.scatter(model.fittedvalues, model.resid)
plt.xlabel('Fitted Values')
plt.ylabel('Residuals')
plt.title('Residuals vs Fitted Values')
plt.tight_layout()
plt.show()

# QQ Plot em plot separado
plt.figure(figsize=(6, 5))
sm.qqplot(model.resid, line='45', fit=True)
plt.title('QQ Plot')
plt.tight_layout()
plt.show()

# Verificação de colinearidade (VIF)
vif_df = pd.DataFrame()
vif_df['Variável'] = X_const.columns
vif_df['VIF'] = [variance_inflation_factor(X_const.values, i) for i in range(X_const.shape[1])]

# Estimativa para o ano de 2015, se disponível
try:
    X_2015 = sm.add_constant(pivot_data.loc[2015, countries_vars])
    Y_pred_2015 = model.predict(X_2015)
    print(f'Estimativa de emissões para 2015: {Y_pred_2015.values[0]}')
except KeyError:
    print('Dados para 2015 não disponíveis.')

# Exibir sumário do modelo
print(model.summary())
print("asd")
# Exibir VIF
print(vif_df)


