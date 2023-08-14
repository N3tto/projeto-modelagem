import streamlit as st

st.set_page_config(
    page_title = "Receita de recife",
    layout = "wide",
    menu_items = {
        'About': '''Este sistema foi desenvolvido pelo prof Gabriel Alves para fins didáticos, para a disciplina de 
        Projeto Interdisciplinar para Sistemas de Informação 3 (PISI3) do 3° período do curso de Bacharelado em Sistemas de Informação
        (BSI) da Universidade Federal Rural de Pernambuco (UFRPE).
        Dúvidas? gabriel.alves@ufrpe.br
        Acesse: bsi.ufrpe.br
        '''
    }
)

st.markdown(f'''
    <h1>Analise de Data Warehouse da Receita de Recife</h1>
    <br>
    <p>
        Este projeto tem o objetivo de analisar, por meio de plotagem de gráficos, um data warehouse montado com os dados da Receita orçamentaria da cidade do Recife.
        Está sendo desenvolvido para a disciplina de Modelagem de Dados da Universidade Federal Rural de Pernambuco, pelos graduandos:
    </p>
    <br>
    <ul>
        <li>Antonio Neto</li>
        <li>Larissa Cerqueira</li>
        <li>Lucas Martins</li>
        <li>Vinícius França</li>
    </ul>
    <br>
''', unsafe_allow_html=True)
