import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go

st.title('Visualização dos dados')

st.subheader('receita.csv')
receita = pd.read_csv('./data/receita.csv')
st.write(receita.shape)
st.write(receita)

st.subheader('responsavel.csv')
responsavel = pd.read_csv('./data/responsavel.csv')
st.write(responsavel.shape)
st.write(responsavel)

st.subheader('fonte.csv')
fonte = pd.read_csv('./data/fonte.csv')
st.write(fonte.shape)
st.write(fonte)

st.subheader('receita_local.csv')
receita_local = pd.read_csv('./data/receita_local.csv')
st.write(receita_local.shape)
st.write(receita_local)

st.subheader('data_receitas.csv')
data_receitas = pd.read_csv('./data/data_receitas.csv')
st.write(data_receitas.shape)
st.write(data_receitas)

st.subheader('categoria_receita.csv')
categoria_receitas = pd.read_csv('./data/categoria_receita.csv')
st.write(categoria_receitas.shape)
st.write(categoria_receitas)

st.subheader('rubrica_receita.csv')
rubrica_receitas = pd.read_csv('./data/rubrica_receita.csv')
st.write(rubrica_receitas.shape)
st.write(rubrica_receitas) 