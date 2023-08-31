import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import mysql.connector
import matplotlib.pyplot as plt


# Função para buscar dados do MySQL
db_connection = mysql.connector.connect(
    host="localhost",
    user="seu_user",
    password="sua_senha.",
    database="seu_database"
)



st.write('1. Como a receita arrecadada tem evoluido ano a ano?')
query = """
SELECT
    dd.ano_nome,
    SUM(fr.receita_arrecadada) AS total_receita_arrecadada
FROM
    dm_data dd
JOIN
    fato_receita fr ON fr.data_id = dd.data_id
GROUP BY
    dd.ano_nome
ORDER BY
    dd.ano_nome;
"""

df = pd.read_sql(query, db_connection)

df['ano_anterior'] = df['total_receita_arrecadada'].shift(1)
df['crescimento'] = (df['total_receita_arrecadada'] / df['ano_anterior']) - 1
average_growth = df['crescimento'].mean() * 100  
st.write(f"Taxa Média de Crescimento Anual: {average_growth:.2f}%")

fig = px.bar(df, x="ano_nome", y="total_receita_arrecadada", title="Evolução da Receita Arrecadada Ano a Ano")
st.plotly_chart(fig)

st.write('2. Quais os meses onde as receitas tendem a serem maiores ')
query = '''
SELECT
    dd.mes_nome AS Mes,
    SUM(fr.receita_arrecadada) AS Total_Receita_Arrecadada 
FROM
    dm_data dd
JOIN
    fato_receita fr ON fr.data_id = dd.data_id
GROUP BY
    dd.mes_nome
ORDER BY Total_Receita_Arrecadada desc;

'''

df = pd.read_sql(query, db_connection)
fig = px.bar(df, x='Mes', y='Total_Receita_Arrecadada', title='Total de Receita Arrecadada por Meses')
st.write(fig)



st.write('3. Quais orgãos estão gerando mais receitas? Há algum orgão que está abaixo das expectativas em relação a receita arrecadada e receita prevista?')
query = """
SELECT
    o.orgao_nome AS Orgao,
    SUM(f.receita_arrecadada) AS Receita_Arrecadada,
    SUM(f.receita_prevista) AS Receita_Prevista
FROM
    fato_receita f
    JOIN dm_responsavel o ON f.orgao_unidade_id = o.orgao_codigo
WHERE
    o.orgao_nome != 'SECRETARIA DE FINANÇAS' AND o.orgao_nome != 'SECRETARIA DE DESENV. SOCIAL, DIREITOS HUMANOS, JUVENTUDE E POLÍTICAS SOBRE DROGAS - ADM. SUPERVISIONADA'
GROUP BY
    o.orgao_nome;
"""

df = pd.read_sql(query, db_connection)
fig = px.bar(df, x="Orgao", y=["Receita_Arrecadada", "Receita_Prevista"], title="Receitas por Órgão (exceto SECRETARIA DE FINANÇAS)")
st.plotly_chart(fig)

#orgaos_abaixo_expectativas = df[df["Receita_Arrecadada"] < df["Receita_Prevista"]]
#if not orgaos_abaixo_expectativas.empty:
    #st.write("Órgãos abaixo das expectativas:")
    #st.dataframe(orgaos_abaixo_expectativas)
#else:
    #st.write("Não há órgãos abaixo das expectativas.")

st.write('4. De quais fontes de origem está vindo o maior valor de receita?')
query = """
SELECT
    fo.fonte_origem_receita_nome AS Fonte_Origem,
    SUM(f.receita_arrecadada) AS Receita_Arrecadada
FROM
    fato_receita f
    JOIN dm_fonte fo ON f.fonte_id = fo.fonte_origem_receita_codigo
WHERE
    fo.fonte_origem_receita_nome NOT IN ('SECRETARIA DE DESENV. SOCIAL, DIREITOS HUMANOS, JUVENTUDE E POLÍTICAS SOBRE DROGAS - ADM. SUPERVISIONADA')    
GROUP BY
    fo.fonte_origem_receita_nome
HAVING
    Receita_Arrecadada > 0
ORDER BY
    SUM(f.receita_arrecadada) DESC;
"""

df = pd.read_sql(query, db_connection)
fig = px.bar(df, x="Fonte_Origem", y="Receita_Arrecadada", title="Fontes de Origem com Maior Valor de Receita")
st.plotly_chart(fig)

st.write('5. Em quais áreas (orgãos, categorias) a receita arrecadada está ABAIXO ou ACIMA da prevista?')

query = """
SELECT dd.ano_nome as Ano, 
	   SUM(fr.receita_arrecadada) as Receita_Arrecadada, 
	   dc.categoria_receita_nome as Categoria, 
       SUM(fr.receita_prevista) as Receita_Prevista
FROM fato_receita AS fr
JOIN dm_data as dd ON dd.data_id = fr.data_id
JOIN dm_categoria as dc ON dc.categoria_id = fr.categoria_id
GROUP BY dd.ano_nome, dc.categoria_receita_nome
order by dd.ano_nome;
"""

df = pd.read_sql(query, db_connection)

df_melted = pd.melt(df, id_vars=['Ano', 'Categoria'], value_vars=['Receita_Arrecadada', 'Receita_Prevista'], 
                    var_name='Metrica', value_name='Valor')

color_map = {'Receita_Arrecadada': 'blue', 'Receita_Prevista': 'green'}
fig = px.bar(df_melted, x='Ano', y='Valor',
             color='Metrica', 
             barmode='group',
             facet_col='Categoria',  
             title='',
             color_discrete_map=color_map)

for annotation in fig['layout']['annotations']: 
    annotation['font'] = dict(size=10) 

fig.for_each_annotation(lambda a: a.update(text=a.text.replace(" ", "<br>")))
st.plotly_chart(fig)




st.write('6. Como as diferentes categorias de receitas vem se comportado ao longo do tempo?')

query = """
SELECT dd.ano_nome as Ano, SUM(fr.receita_arrecadada) as Receita_Arrecadada, dc.categoria_receita_nome as categoria_receita_nome
FROM fato_receita AS fr
JOIN dm_data as dd ON dd.data_id = fr.data_id
JOIN dm_categoria as dc ON dc.categoria_id = fr.categoria_id
GROUP BY dd.ano_nome, dc.categoria_receita_nome
order by dd.ano_nome;
"""

df = pd.read_sql(query, db_connection)

df['Ano'] = df['Ano'].astype(int)  
df = df.sort_values(['categoria_receita_nome', 'Ano'])
df['crescimento_ano_a_ano'] = df.groupby('categoria_receita_nome')['Receita_Arrecadada'].pct_change() * 100  
media_crescimento = df.groupby('categoria_receita_nome')['crescimento_ano_a_ano'].mean()
st.write("Média de crescimento ano após ano para cada categoria:")
st.write(media_crescimento)

fig = px.line(df, x='Ano', y='Receita_Arrecadada', color='categoria_receita_nome', title='Crescimento da Receita por Categoria ao Longo dos Anos')
st.plotly_chart(fig)
