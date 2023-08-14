import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

receita = pd.read_csv('./data/receita.csv')
responsavel = pd.read_csv('./data/responsavel.csv')
fonte = pd.read_csv('./data/fonte.csv')
receita_local = pd.read_csv('./data/receita_local.csv')
data_receitas = pd.read_csv('./data/data_receitas.csv')
categoria_receitas = pd.read_csv('./data/categoria_receita.csv')
rubrica_receitas = pd.read_csv('./data/rubrica_receita.csv')

st.write('1. Como a receita arrecadada tem evoluido ano a ano? Há algum mes especifico que tende a ter receitas mais altas ou mais baixas?')
# receita = receita.groupby(['ano', 'mes'])['receita_arrecadada'].mean().reset_index()

# fig = px.line(receita, x='mes', y='receita_prevista', color='ano', title='Evolução da Receita Mensal por Ano')
# fig.update_layout(xaxis_title='Mês', yaxis_title='Receita')
# st.write(fig)


st.write('2. Quais são as categorias de receita que mais contribuem para a receita total? Há mudanças nas categorias de receita predominantes ao longo do tempo? ')
st.write(receita)
st.write(categoria_receitas)
receita_categoria = pd.concat([receita, categoria_receitas['categoria_receita_nome']], axis=1)
st.write(receita_categoria)

total_revenue_per_category = receita_categoria.groupby('categoria_receita_nome')['receita_prevista'].sum()
fig = px.bar(total_revenue_per_category, x='categoria_receita_nome', y='receita_prevista', title='Receita Total por Categoria')
fig.update_layout(xaxis_title='Categoria', yaxis_title='Receita Total')
st.write(fig)


st.write('3. Quais orgãos estão gerando mais receitas? Há algum orgão que está abaixo das expectativas em relação a receita arrecadada e receita prevista?')
st.write('4. De quais fontes de origem está vindo o maior valor de receita?')
st.write('5. Em quais áreas (orgãos, categorias) a receita arrecadada está ABAIXO ou ACIMA da prevista?')
st.write('6. Alguma coisa em cima da receita prevista e arrecadada.. como isso vem se comportando ao longo do tempo.')