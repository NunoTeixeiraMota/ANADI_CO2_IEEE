import pandas as pd

# Carregar os dados de emissões de CO2
caminho_dados_co2 = './CO_data.csv'
dados_co2 = pd.read_csv(caminho_dados_co2)

# 
#%%
import matplotlib.pyplot as plt

# Filtrar dados para Portugal
dados_co2_portugal = dados_co2[dados_co2['country'] == 'Portugal']

# Plotar as emissões totais de CO2 de Portugal (1900-2021)
plt.figure(figsize=(12, 6))
plt.plot(dados_co2_portugal['year'], dados_co2_portugal['co2'], marker='o', linestyle='-', markersize=4)
plt.xlabel('Year')
plt.ylabel('CO2 (MtCO2)')
plt.grid(True)
plt.show()

# Encontrar o ano com emissões máximas
ano_max_emissoes = dados_co2_portugal.loc[dados_co2_portugal['co2'].idxmax()]
informacao_ano_max_emissoes = (ano_max_emissoes['year'], ano_max_emissoes['co2'])

informacao_ano_max_emissoes

#%%
# Plotar emissões de CO2 de diferentes fontes em Portugal (1900-2021)
plt.figure(figsize=(14, 8))

# Fontes: cimento, carvão, queimada, gás, óleo
plt.plot(dados_co2_portugal['year'], dados_co2_portugal['cement_co2'], label='Cement', marker='', linestyle='-')
plt.plot(dados_co2_portugal['year'], dados_co2_portugal['coal_co2'], label='Coal', marker='', linestyle='-')
plt.plot(dados_co2_portugal['year'], dados_co2_portugal['flaring_co2'], label='Flaring', marker='', linestyle='-')
plt.plot(dados_co2_portugal['year'], dados_co2_portugal['gas_co2'], label='Gas', marker='', linestyle='-')
plt.plot(dados_co2_portugal['year'], dados_co2_portugal['oil_co2'], label='Oil', marker='', linestyle='-')

plt.xlabel('Year')
plt.ylabel('CO2 (MtCO2)')
plt.legend()
plt.grid(True)
plt.show()

#%%
# Filtrar dados para Espanha
dados_co2_espanha = dados_co2[dados_co2['country'] == 'Spain']

# Calcular emissões de CO2 per capita para Portugal e Espanha
co2_per_capita_portugal = dados_co2_portugal['co2'] / dados_co2_portugal['population'] * 1e6  # Converter para toneladas métricas
co2_per_capita_espanha = dados_co2_espanha['co2'] / dados_co2_espanha['population'] * 1e6  # Converter para toneladas métricas

# Plotar comparação das emissões de CO2 per capita entre Portugal e Espanha (1900-2021)
plt.figure(figsize=(14, 8))
plt.plot(dados_co2_portugal['year'], co2_per_capita_portugal, label='Portugal', marker='', linestyle='-')
plt.plot(dados_co2_espanha['year'], co2_per_capita_espanha, label='Spain', marker='', linestyle='-')

plt.xlabel('Year')
plt.ylabel('CO2 Per Capita (MtCO2)')
plt.legend()
plt.grid(True)
plt.show()

#%%
# Filtrar dados para os países especificados e período (2000-2021)
paises = ['United States', 'China', 'India', 'European Union (27)', 'Russia']
dados_co2_filtrados = dados_co2[(dados_co2['country'].isin(paises)) & (dados_co2['year'] >= 2000)]

# Plotar comparação das emissões de CO2 originárias do carvão
plt.figure(figsize=(14, 8))
for pais in paises:
    dados_pais = dados_co2_filtrados[dados_co2_filtrados['country'] == pais]
    plt.plot(dados_pais['year'], dados_pais['coal_co2'], label=pais, marker='', linestyle='-')

plt.xlabel('Year')
plt.ylabel('Coal CO2 (MtCO2)')
plt.legend()
plt.grid(True)
plt.show()
#%%
# Carregar os dados de emissões de CO2
caminho_dados_co2 = './CO_data.csv'
dados_co2 = pd.read_csv(caminho_dados_co2)

# Filtrar dados para os países e período especificados
paises = ['United States', 'China', 'India', 'European Union (27)', 'Russia']
dados_filtrados = dados_co2[(dados_co2['country'].isin(paises)) & (dados_co2['year'] >= 2000) & (dados_co2['year'] <= 2021)]

# Calcular as médias das emissões de CO2 devidas a cimento, carvão, queima (flaring), gás, metano, óxido nitroso e petróleo
media_emissoes = dados_filtrados.groupby('country').agg({
    'cement_co2': 'mean',
    'coal_co2': 'mean',
    'flaring_co2': 'mean',
    'gas_co2': 'mean',
    'methane': 'mean',
    'nitrous_oxide': 'mean',
    'oil_co2': 'mean'
}).reset_index()

# Formatar as entradas da tabela para terem apenas 3 casas decimais
media_emissoes = media_emissoes.round(3)

# Exibir a tabela
print(media_emissoes)
