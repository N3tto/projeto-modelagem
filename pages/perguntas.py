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
    password="sua_senha",
    database="seu_database"
)

########################################
#                                      #
#               Pergunta 1             #
#                                      #
########################################

st.write('1. Como a receita arrecadada tem evoluido ano a ano?')
min_year, max_year = st.slider("Selecione a faixa de anos:", 2002, 2023, (2002, 2023))
query = f"""
    SELECT
        dd.ano_nome,
        SUM(fr.receita_arrecadada) AS total_receita_arrecadada
    FROM
        dm_data dd
    JOIN
        fato_receita fr ON fr.data_id = dd.data_id
    WHERE
        dd.ano_nome BETWEEN {min_year} AND {max_year}
    GROUP BY
        dd.ano_nome
    ORDER BY
        dd.ano_nome;
    """

df = pd.read_sql(query, db_connection)

df['ano_anterior'] = df['total_receita_arrecadada'].shift(1)
df['crescimento'] = (df['total_receita_arrecadada'] / df['ano_anterior']) - 1

for column in ['total_receita_arrecadada']:
    mean_value = df[column].mean()
    df[column].replace(0, mean_value, inplace=True)
average_growth = df['crescimento'].mean() * 100  


st.write(f"Taxa Média de Crescimento Anual: {average_growth:.2f}%")

fig1 = px.bar(df, x="ano_nome", y="total_receita_arrecadada", title="Evolução da Receita Arrecadada Ano a Ano")
st.plotly_chart(fig1)


########################################
#                                      #
#               Pergunta 2             #
#                                      #
########################################


st.write('2. Quais os meses onde as receitas tendem a serem maiores ')
min_year, max_year = st.slider("Selecione a faixa de anos:", 2002, 2023, (2005, 2020))

todos_meses = ["Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho",
                   "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"]
meses_selecionados = st.multiselect("Selecione os meses:", todos_meses, default=todos_meses)

meses_str = "', '".join(meses_selecionados)

query = f"""
    SELECT
        dd.mes_nome AS Mes,
        SUM(fr.receita_arrecadada) AS Total_Receita_Arrecadada 
    FROM
        dm_data dd
    JOIN
        fato_receita fr ON fr.data_id = dd.data_id
    WHERE
        dd.ano_nome BETWEEN {min_year} AND {max_year}
        AND dd.mes_nome IN ('{meses_str}')
    GROUP BY
        dd.mes_nome
    ORDER BY Total_Receita_Arrecadada DESC;
    """

df = pd.read_sql(query, db_connection)

for column in ['Total_Receita_Arrecadada']:
    mean_value = df[column].mean()
    df[column].replace(0, mean_value, inplace=True)

fig2 = px.bar(df, x='Mes', y='Total_Receita_Arrecadada', title='Total de Receita Arrecadada por Meses')
fig2.update_yaxes(tickvals=[0, 500e6, 1e9, 1.5e9, 2e9, 2.5e9, 3e9, 3.5e9, 4e9, 4.5e9, 5e9, 5.5e9, 6e9, 6.5e9, 7e9, 7.5e9, 8e9],
                ticktext=['0', '500M', '1B', '1.5B', '2B', '2.5B', '3B', '3.5B', '4B', '4.5B', '5B', '5.5B', '6B', '6.5B', '7B', '7.5B', '8B'])
st.plotly_chart(fig2)


########################################
#                                      #
#               Pergunta 3             #
#                                      #
########################################


st.write('3. Quais orgãos estão gerando mais receitas? Há algum orgão que está abaixo das expectativas em relação a receita arrecadada e receita prevista?')

query_orgaos = """
SELECT DISTINCT orgao_nome 
FROM dm_responsavel
WHERE orgao_nome != 'SECRETARIA DE FINANÇAS' 
AND orgao_nome != 'SECRETARIA DE DESENV. SOCIAL, DIREITOS HUMANOS, JUVENTUDE E POLÍTICAS SOBRE DROGAS - ADM. SUPERVISIONADA';
"""
df_orgaos = pd.read_sql(query_orgaos, db_connection)
df_orgaos['orgao_nome'] = df_orgaos['orgao_nome'].str.encode('utf-8').str.decode('utf-8')
all_orgaos = df_orgaos['orgao_nome'].tolist()

selected_orgaos = st.multiselect('Selecione os Órgãos:', options=all_orgaos, default=all_orgaos)

selected_orgaos_str = ', '.join([f"'{orgao}'" for orgao in selected_orgaos])

if selected_orgaos:
    selected_orgaos_str = ', '.join([f"'{orgao}'" for orgao in selected_orgaos])
    query = f"""
    SELECT
        o.orgao_nome AS Orgao,
        SUM(f.receita_arrecadada) AS Receita_Arrecadada,
        SUM(f.receita_prevista) AS Receita_Prevista
    FROM
        fato_receita f
        JOIN dm_responsavel o ON f.orgao_unidade_id = o.orgao_codigo
    WHERE
        o.orgao_nome IN ({selected_orgaos_str})
        AND o.orgao_nome != 'SECRETARIA DE FINANÇAS' 
        AND o.orgao_nome != 'SECRETARIA DE DESENV. SOCIAL, DIREITOS HUMANOS, JUVENTUDE E POLÍTICAS SOBRE DROGAS - ADM. SUPERVISIONADA'
    GROUP BY
        o.orgao_nome;
    """

    df = pd.read_sql(query, db_connection)
    for column in ['Receita_Arrecadada', 'Receita_Prevista']:
        mean_value = df[column].mean()
        df[column].replace(0, mean_value, inplace=True)


    fig3 = px.bar(df, x="Orgao", y=["Receita_Arrecadada", "Receita_Prevista"], title="Receitas por Órgão")
    fig3.update_layout(
        autosize=False,
        width=1500,
        height=1000
    )
    fig3.update_xaxes(tickangle=45)
    st.plotly_chart(fig3)
else:
    st.warning("Por favor, selecione pelo menos um órgão.")

########################################
#                                      #
#               Pergunta 4             #
#                                      #
########################################
st.write('4. De quais fontes de origem está vindo o maior valor de receita?')
query_fontes = """
SELECT DISTINCT fonte_origem_receita_nome 
FROM dm_fonte
WHERE fonte_origem_receita_nome NOT IN ('SECRETARIA DE DESENV. SOCIAL, DIREITOS HUMANOS, JUVENTUDE E POLÍTICAS SOBRE DROGAS - ADM. SUPERVISIONADA');
"""
df_fontes = pd.read_sql(query_fontes, db_connection)
all_fontes = df_fontes['fonte_origem_receita_nome'].tolist()

selected_fontes = st.multiselect('Selecione as Fontes de Origem:', options=all_fontes, default=all_fontes)
if not selected_fontes:
    st.warning("Por favor, selecione pelo menos uma Fonte de Origem para visualizar os dados.")
else:
    selected_fontes_str = ', '.join([f"'{fonte}'" for fonte in selected_fontes])

    query = f"""
    SELECT
        fo.fonte_origem_receita_nome AS Fonte_Origem,
        SUM(f.receita_arrecadada) AS Receita_Arrecadada
    FROM
        fato_receita f
        JOIN dm_fonte fo ON f.fonte_id = fo.fonte_origem_receita_codigo
    WHERE
        fo.fonte_origem_receita_nome IN ({selected_fontes_str})
    GROUP BY
        fo.fonte_origem_receita_nome
    HAVING
        Receita_Arrecadada > 0
    ORDER BY
        SUM(f.receita_arrecadada) DESC;
    """

    df = pd.read_sql(query, db_connection)
    for column in ['Receita_Arrecadada']:
        mean_value = df[column].mean()
        df[column].replace(0, mean_value, inplace=True)

    fig4 = px.bar(df, x="Fonte_Origem", y="Receita_Arrecadada", title="Fontes de Origem com Maior Valor de Receita")

    fig4.update_layout(
        autosize=False,
        width=1500,
        height=1000
    )
    fig4.update_xaxes(tickangle=45)

    st.plotly_chart(fig4)

########################################
#                                      #
#               Pergunta 5             #
#                                      #
########################################

st.write('5. Em quais áreas (orgãos, categorias) a receita arrecadada está ABAIXO ou ACIMA da prevista?')

start_year = st.selectbox('Ano de início:', list(range(2002, 2024)), index=0)
end_year = st.selectbox('Ano de fim:', list(range(2002, 2024)), index=21)

query_categorias = "SELECT DISTINCT categoria_receita_nome FROM dm_categoria;"
df_categorias = pd.read_sql(query_categorias, db_connection)
all_categorias = df_categorias['categoria_receita_nome'].tolist()

selected_categorias = st.multiselect('Selecione as Categorias:', options=all_categorias, default=all_categorias)
selected_categorias_str = ', '.join([f"'{categoria}'" for categoria in selected_categorias])

if not selected_categorias:
    st.warning("Por favor, selecione pelo menos uma categoria para visualizar os dados.")
else:
    query = f"""
    SELECT dd.ano_nome as Ano, 
           SUM(fr.receita_arrecadada) as Receita_Arrecadada, 
           dc.categoria_receita_nome as Categoria, 
           SUM(fr.receita_prevista) as Receita_Prevista
    FROM fato_receita AS fr
    JOIN dm_data as dd ON dd.data_id = fr.data_id
    JOIN dm_categoria as dc ON dc.categoria_id = fr.categoria_id
    WHERE dd.ano_nome BETWEEN {start_year} AND {end_year}
    AND dc.categoria_receita_nome IN ({selected_categorias_str})
    GROUP BY dd.ano_nome, dc.categoria_receita_nome
    ORDER BY dd.ano_nome;
    """

    df = pd.read_sql(query, db_connection)
    for column in ['Receita_Arrecadada', 'Receita_Prevista']:
        mean_value = df[column].mean()
        df[column].replace(0, mean_value, inplace=True)

    df_melted = pd.melt(df, id_vars=['Ano', 'Categoria'], value_vars=['Receita_Arrecadada', 'Receita_Prevista'],
                        var_name='Metrica', value_name='Valor')

    color_map = {'Receita_Arrecadada': 'blue', 'Receita_Prevista': 'green'}
    fig = px.bar(df_melted, x='Ano', y='Valor',
                 color='Metrica',
                 barmode='group',
                 facet_col='Categoria',
                 title='')

    fig.update_layout(
        autosize=False,
        width=1500,
        height=1000
    )

    for annotation in fig['layout']['annotations']:
        annotation['font'] = dict(size=10)

    fig.for_each_annotation(lambda a: a.update(text=a.text.replace(" ", "<br>")))

    st.plotly_chart(fig)

########################################
#                                      #
#               Pergunta 6             #
#                                      #
########################################

st.write('6. Como as diferentes categorias de receitas vêm se comportando ao longo do tempo?')

start_year = st.selectbox('Ano de início:', list(range(2002, 2024)), index=0, key='start_year_6')
end_year = st.selectbox('Ano de fim:', list(range(2002, 2024)), index=21, key='end_year_6')

query_categorias = "SELECT DISTINCT categoria_receita_nome FROM dm_categoria;"
df_categorias = pd.read_sql(query_categorias, db_connection)
all_categorias = df_categorias['categoria_receita_nome'].tolist()

selected_categorias = st.multiselect('Selecione as Categorias:', options=all_categorias, default=all_categorias, key='selected_cateogrias_6')

if not selected_categorias:
    st.warning("Por favor, selecione pelo menos uma categoria para visualizar os dados.")
else:
    selected_categorias_str = ', '.join([f"'{categoria}'" for categoria in selected_categorias])

    query = f"""
    SELECT dd.ano_nome as Ano, 
           SUM(fr.receita_arrecadada) as Receita_Arrecadada, 
           dc.categoria_receita_nome as categoria_receita_nome
    FROM fato_receita AS fr
    JOIN dm_data as dd ON dd.data_id = fr.data_id
    JOIN dm_categoria as dc ON dc.categoria_id = fr.categoria_id
    WHERE dd.ano_nome BETWEEN {start_year} AND {end_year}
    AND dc.categoria_receita_nome IN ({selected_categorias_str})
    GROUP BY dd.ano_nome, dc.categoria_receita_nome
    ORDER BY dd.ano_nome;
    """

    df = pd.read_sql(query, db_connection)
    for column in ['Receita_Arrecadada']:
        mean_value = df[column].mean()
        df[column].replace(0, mean_value, inplace=True)

    if df.empty:
        st.warning("Nenhum dado disponível para as opções selecionadas.")
    else:
        df['Ano'] = df['Ano'].astype(int)
        df = df.sort_values(['categoria_receita_nome', 'Ano'])
        df['crescimento_ano_a_ano'] = df.groupby('categoria_receita_nome')['Receita_Arrecadada'].pct_change() * 100
        media_crescimento = df.groupby('categoria_receita_nome')['crescimento_ano_a_ano'].mean()
        st.write("Média de crescimento ano após ano para cada categoria:")
        st.write(media_crescimento)

        fig6 = px.line(df, x='Ano', y='Receita_Arrecadada', color='categoria_receita_nome', title='Crescimento da Receita por Categoria ao Longo dos Anos')
        st.plotly_chart(fig6)