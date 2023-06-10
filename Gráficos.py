'''Código utilizado para montar 4 tipos diferentes de grádicos sendo eles:
• Ranking
• Setores
• Densidade utilizando mapa
• Trremap'''

# Importação de biliotecas
import matplotlib.pyplot as plt
import plotly.express as px
import geopandas as gpd
import pandas as pd
import numpy as np

# Tratamento de dados
dataset = pd.read_csv('inscricoes_juventude_digital_2023-01.csv', encoding='latin-1', sep=';', header=0) # Leitura
dataset['Tipo de ensino'] = dataset['Estudante de escola pública'].map({'SIM': 'Ensino Público', 'NAO': 'Ensino Privado'}) # Ajuste de informações

'''RANKING DE ESCOLARIDADE DOS INSCRITOS 
Esse gráfico visa mostrar a o nível de escolaridades dos inscritos nos cursos do Juventude Digital(JD) nos cursos em 2023.1
'''
contagem_escolaridade = dataset['Escolaridade'].value_counts() # Contagem de Jovens por escolaridade
plt.figure(figsize=(16, 8)) # Tamanho do Gráfico
plt.barh(contagem_escolaridade.index[::-1], contagem_escolaridade.values[::-1], color = '#FFB800') # Construção do gráfico 

# Personalização do gráfico
plt.xlabel('Número de Inscritos')
plt.ylabel('Nível de Escolaridade')
plt.title('Ranking de Escolaridade dos Inscritos de 2023.1')
plt.tight_layout()

# Exibição do gráfico
plt.show()

'''GRÁFICO DE SETORES
Vem destacar a participação dos jovens oriundos do ensino público
'''
labels = dataset['Tipo de ensino'].unique() # Categorias

# Define o tamnho de cada categoria
sizes = np.zeros_like(labels) 
for i in range(labels.size):
    sizes[i] = np.sum(dataset['Tipo de ensino'] == labels[i])

# Personalização do gráfico
labels = ['Privado', 'Público','']
plt.pie(sizes, labels=labels, colors=['#16B4EA','#F57D2C'])
plt.title('Participação do Jovens de Ensino Público nos cursos do Juventude Digital em 2023.1')

# Exibição do gráfico
plt.show()

''''MAPA POR BAIRRO
Tem o bjetivo de evidenciar de quais bairros são esse jovens.
'''
# Caminho para o arquivo .shp
shapefile_path = 'Mapa de Fortaleza\\bairros.shp'

# Contagem de jovens por bairro
contagem_jovens = dataset['Bairro'].value_counts().reset_index()
contagem_jovens.columns = ['nome_bairro', 'count']

# Cria um novo subplot com tamanho ajustado
bairros = gpd.read_file(shapefile_path)
fig, ax = plt.subplots(figsize=(180,100))

# Plota o mapa dos bairros
bairros.plot(ax=ax, color='lightgray', edgecolor='gray')
dados_combinados = bairros.merge(contagem_jovens, left_on='nome_bairr', right_on='nome_bairro', how='left')
dados_combinados.plot(column='count', ax=ax, cmap='Blues', linewidth=0.8, edgecolor='k', legend=True)
for x, y, label in zip(dados_combinados.geometry.centroid.x, dados_combinados.geometry.centroid.y, dados_combinados['nome_bairr']):
    plt.annotate(label, xy=(x, y), xytext=(0, 0), textcoords="offset points", fontsize=3)

# Exibição do mapa
ax.set_title('Mapa de Inscrições dos Jovens por Bairro')
ax.axis('off')
plt.show()

'''TREEMAP
Monta o perfil desse jovens por tipo de ensino oriundo, sexo e escolaridade  
'''
# Agrupa as categorias desejadas numa raiz comum
agrupado = dataset.groupby(['Tipo de ensino', 'Genero', 'Escolaridade']).size().reset_index(name='count')
agrupado['label'] = agrupado['Tipo de ensino'] + ' - ' + agrupado['Genero'] + ' - ' + agrupado['Escolaridade']

# Ordena a ordem a ordem dos dados
agrupado = agrupado.sort_values('count', ascending=False)
sizes = agrupado['count'].values.tolist()

# Personaçização
fig = px.treemap(agrupado, path=['label'], values='count', color='count')
fig.update_layout(title='Perfil dos Inscritos de 2023.1')

# Exibição do Treemap
fig.show()
