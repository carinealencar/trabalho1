import streamlit as st
import pandas as pd
import os
import plotly.express as px
import json

st.set_page_config(
    page_title="Dashboard das notas do Enem nos últimos anos",
    page_icon="📊",
    layout="centered",
    initial_sidebar_state="expanded"
)

FILE_PATHS = {
    '2020': 'ENEM_2020_FILTRADO_LIMPO.zip',
    '2021': 'ENEM_2021_FILTRADO_LIMPO.zip',
    '2022': 'ENEM_2022_FILTRADO_LIMPO.zip',
    '2023': 'ENEM_2023_FILTRADO_LIMPO.zip'
}

@st.cache_data
def load_geojson(path):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)
geojson_municipios = load_geojson('municipios_ibge.geojson.json')


@st.cache_data
def load_data(path):
    return pd.read_csv(
        path,
        sep=';',
        encoding='latin1',
        compression='zip',
        low_memory=False
    )
    
st.title('Dashboard das notas do Enem nos últimos anos 📊')
st.header('Filtros:')

ano = st.selectbox('Escolha o ano para a análise:', 
                   ('2020', '2021', '2022', '2023'))
filtro = st.selectbox('Escolha uma variável para análise:', 
                      sorted(['Renda', 'Raça']))

if filtro == 'Renda':
    salario = st.selectbox(
        'Escolha a faixa salarial:',
        ['Nenhuma renda', 'Até 1 salário mínimo', 'Entre 1 e 3 salários mínimos', 'Entre 3 e 6 salários mínimos', 'Acima de 6 salários mínimos'])

if filtro == 'Raça':
    raca = st.selectbox(
        'Escolha a raça a analisar:',
        ['Preto', 'Pardo', 'Branco', 'Indígena', 'Amarelo', 'Não declarado']) 

m_renda = {
    'Nenhuma renda': ['A'],
    'Até 1 salário mínimo': ['B'],
    'Entre 1 e 3 salários mínimos': ['C', 'D'],
    'Entre 3 e 6 salários mínimos': ['E', 'F', 'G'],
    'Acima de 6 salários mínimos': ['H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q']
}

m_raca = {
    'Branco': 1,
    'Preto': 2,
    'Pardo': 3,
    'Amarelo': 4,
    'Indígena': 5,
    'Não declarado': 0
}

m_faixa_etaria = {
    1: 'Menor de 17 anos',
    2: '17 anos',
    3: '18 anos',
    4: '19 anos',
    5: '20 anos',
    6: '21 anos',
    7: '22 anos',
    8: '23 anos',
    9: '24 anos',
    10: '25 anos',
    11: '26 a 30 anos',
    12: '31 a 35 anos',
    13: '36 a 40 anos',
    14: '41 a 45 anos',
    15: '46 a 50 anos',
    16: '51 a 55 anos',
    17: '56 a 60 anos',
    18: '61 a 65 anos',
    19: '66 a 70 anos',
    20: 'Maior de 70 anos'
}

botao = st.button('Exibir gráficos')

