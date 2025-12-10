import streamlit as st
import os

st.set_page_config(
    page_title="Dashboard das notas do Enem nos últimos 5 anos",
    page_icon="📊",
    layout="centered",
    initial_sidebar_state="expanded"
)

st.title('Dashboard das notas do Enem nos últimos 5 anos 📊')

ano = st.radio('Escolha o ano para a análise:'
                    ('2020', '2021', '2022', '2023', '2024'))

filtro = st.selectbox('Escolha uma variável para análise:',
                                    sorted(['Renda', 'Ano de conclusão', 'Raça']))

if filtro == 'Renda':
    salario = st.radio('R$1.420', 'Entre R$1.420 e R$2840', '2022', '2023', '2024')
