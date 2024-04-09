import pandas as pd

# Carregar os dados de emissões de CO2
caminho_dados_co2 = 'CO_data.csv'
co_data = pd.read_csv(caminho_dados_co2)


#%%

import numpy as np
from scipy import stats

# Definindo a seed e criando a amostra aleatória de anos
np.random.seed(100)
years = pd.Series([i for i in range(1900, 2022)])
sampleyears1 = years.sample(n=30, replace=False).sort_values()

# Filtrar os dados para Portugal e Hungria
co_data_filtered = co_data[(co_data['country'] == 'Portugal') | (co_data['country'] == 'Hungary')]

# Filtrar os dados para os anos selecionados na amostra
co_data_sample = co_data_filtered[co_data_filtered['year'].isin(sampleyears1)]

# Separar os dados de PIB para Portugal e Hungria
portugal_gdp = co_data_sample[co_data_sample['country'] == 'Portugal']['gdp'].dropna()
hungary_gdp = co_data_sample[co_data_sample['country'] == 'Hungary']['gdp'].dropna()

# Realizar um teste t para comparar as médias
t_stat, p_value = stats.ttest_ind(portugal_gdp, hungary_gdp, equal_var=False, alternative='greater')

t_stat, p_value

# Realizamos este teste anteriormente. Vou exibir uma conclusão baseada no p-valor.
if p_value < 0.05:
    print(f"Há evidência estatística (p-valor = {p_value:.4f}) para afirmar que a média do PIB de Portugal é superior à da Hungria.")
else:
    print(f"Não há evidência estatística suficiente (p-valor = {p_value:.4f}) para afirmar que a média do PIB de Portugal é superior à da Hungria.")



#%%

# Definindo as seeds e criando as amostras aleatórias de anos para Portugal e Hungria
np.random.seed(55)
sampleyears2 = years.sample(n=12, replace=False).sort_values()
np.random.seed(85)
sampleyears3 = years.sample(n=12, replace=False).sort_values()

# Filtrando os dados para os anos em cada amostra para Portugal e Hungria
portugal_gdp_sample2 = co_data[(co_data['country'] == 'Portugal') & (co_data['year'].isin(sampleyears2))]['gdp'].dropna()
hungary_gdp_sample3 = co_data[(co_data['country'] == 'Hungary') & (co_data['year'].isin(sampleyears3))]['gdp'].dropna()

# Realizando um teste t para comparar as médias de sampleyears2 e sampleyears3
t_stat_2, p_value_2 = stats.ttest_ind(portugal_gdp_sample2, hungary_gdp_sample3, equal_var=False, alternative='greater')

t_stat_2, p_value_2

# Baseado no segundo teste t realizado. Vou exibir uma conclusão semelhante.
if p_value_2 < 0.05:
    print(f"Há evidência estatística (p-valor = {p_value_2:.4f}) para afirmar que, nas amostras selecionadas, a média do PIB de Portugal é superior à da Hungria.")
else:
    print(f"Não há evidência estatística suficiente (p-valor = {p_value_2:.4f}) para afirmar que, nas amostras selecionadas, a média do PIB de Portugal é superior à da Hungria.")




#%%

import matplotlib.pyplot as plt

# Filtrando os dados de CO2 para os anos em sampleyears2 e para as regiões especificadas
regions = ['United States', 'Russia', 'China', 'India', 'European Union (27)']
co2_data_filtered = co_data[co_data['country'].isin(regions) & co_data['year'].isin(sampleyears2)]

# Agregando as emissões de CO2 para cada região nos anos selecionados
co2_emissions_by_region = co2_data_filtered.groupby(['country', 'year'])['co2'].sum().reset_index()

# Preparando os dados para ANOVA
co2_emissions_us = co2_emissions_by_region[co2_emissions_by_region['country'] == 'United States']['co2'].dropna()
co2_emissions_russia = co2_emissions_by_region[co2_emissions_by_region['country'] == 'Russia']['co2'].dropna()
co2_emissions_china = co2_emissions_by_region[co2_emissions_by_region['country'] == 'China']['co2'].dropna()
co2_emissions_india = co2_emissions_by_region[co2_emissions_by_region['country'] == 'India']['co2'].dropna()
# A União Europeia (27) pode não estar diretamente disponível nos dados, ajustar conforme necessário.

# Realizando ANOVA para testar diferenças entre as emissões de CO2 das regiões
f_stat_3, p_value_3 = stats.f_oneway(co2_emissions_us, co2_emissions_russia, co2_emissions_china, co2_emissions_india)

f_stat_3, p_value_3

# Baseado na ANOVA realizada. Vou exibir uma conclusão baseada no p-valor.
if p_value_3 < 0.05:
    print(f"Há diferenças significativas nas emissões totais de CO2 entre as regiões especificadas (p-valor = {p_value_3:.4f}).")
else:
    print(f"Não há diferenças significativas nas emissões totais de CO2 entre as regiões especificadas (p-valor = {p_value_3:.4f}).")


from statsmodels.stats.multicomp import pairwise_tukeyhsd

# Preparando os dados para a análise post-hoc
# Necessitamos juntar todos os dados de emissão em uma única lista e uma lista correspondente de rótulos de grupo (país)
emissions_data = np.concatenate([co2_emissions_us, co2_emissions_russia, co2_emissions_china, co2_emissions_india])
groups = ['United States'] * len(co2_emissions_us) + ['Russia'] * len(co2_emissions_russia) + ['China'] * len(co2_emissions_china) + ['India'] * len(co2_emissions_india)

# Realizando o teste de Tukey HSD
tukey_results = pairwise_tukeyhsd(endog=emissions_data, groups=groups, alpha=0.05)


# Realizando o teste de Tukey HSD e preparando para o plot
tukey_results = pairwise_tukeyhsd(endog=emissions_data, groups=groups, alpha=0.05)

# Plotando os resultados do teste de Tukey HSD
tukey_results.plot_simultaneous()
plt.show()

