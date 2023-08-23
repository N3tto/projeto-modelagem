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
    user="seu_root",
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
    dd.ano_nome;
"""

df = pd.read_sql(query, db_connection)
#db_connection.close()
fig = px.bar(df, x="ano_nome", y="total_receita_arrecadada", title="Evolução da Receita Arrecadada Ano a Ano")
st.plotly_chart(fig)

st.write('2. Quais são as categorias de receita que mais contribuem para a receita total? Há mudanças nas categorias de receita predominantes ao longo do tempo? ')
# Consulta para obter as categorias de receita que mais contribuem para a receita total



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
    o.orgao_nome != 'SECRETARIA DE FINANÇAS'
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
# Consulta para obter órgãos e categorias com receita arrecadada e prevista
query = """
SELECT
    r.orgao_nome AS Orgao,
    c.categoria_receita_nome AS Categoria,
    SUM(f.receita_arrecadada) AS Receita_Arrecadada,
    SUM(f.receita_prevista) AS Receita_Prevista
FROM
    fato_receita f
    JOIN dm_responsavel r ON f.orgao_unidade_id = r.orgao_codigo
    JOIN dm_categoria c ON f.categoria_id = c.categoria_receita_codigo
GROUP BY
    r.orgao_nome,
    c.categoria_receita_nome;
"""




st.write('6. Alguma coisa em cima da receita prevista e arrecadada.. como isso vem se comportando ao longo do tempo.')

