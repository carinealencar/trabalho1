import streamlit as st
import pandas as pd
import os
import plotly.express as px

st.set_page_config(
    page_title="Dashboard das notas do Enem nos últimos anos",
    page_icon="📊",
    layout="centered",
    initial_sidebar_state="expanded"
)

FILE_PATHS = {
    '2020': 'ENEM_2020_FILTRADO_AMOSTRA.csv',
    '2021': 'ENEM_2021_FILTRADO_AMOSTRA.csv',
    '2022': 'ENEM_2022_FILTRADO_AMOSTRA.csv',
    '2023': 'ENEM_2023_FILTRADO_AMOSTRA.csv'
}

@st.cache_data
def load_data(path):
    df = pd.read_csv(path, sep=';', encoding='latin1')
    return df

st.title('Dashboard das notas do Enem nos últimos anos 📊')
st.header('Filtros:')

ano = st.selectbox('Escolha o ano para a análise:', 
                   ('2020', '2021', '2022', '2023'))
filtro = st.selectbox('Escolha uma variável para análise:', 
                      sorted(['Renda', 'Ano de conclusão', 'Raça']))

if filtro == 'Renda':
    salario = st.selectbox(
        'Escolha a faixa salarial:',
        ['Até 1 salário mínimo', 'Entre 1 e 3 salários mínimos', 'Entre 3 e 6 salários mínimos', 'Acima de 6 salários mínimos'])

if filtro == 'Ano de conclusão':
    ano_c = st.selectbox(
        'Escolha o período do ano de conclusão:',
        ['Entre 2007 e 2012', 'Entre 2013 e 2018', 'Entre 2019 e 2023'])

if filtro == 'Raça':
    raca = st.selectbox(
        'Escolha a raça a analisar:',
        ['Preto', 'Pardo', 'Branco', 'Indígena', 'Amarelo', 'Não informado'])

botao = st.button('Exibir gráficos')

if botao:
    st.subheader(f"Processando Dados do ENEM {ano}")
    caminho_arquivo = FILE_PATHS[ano]

    st.subheader(f"Resultados e Análise do ENEM {ano}")
    st.write(f"Total de participantes para a análise: **{len(caminho_arquivo)}**")

    col1, col2 = st.columns([1, 2])
    with col1:
        
    with col2:
        
