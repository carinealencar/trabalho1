import streamlit as st
import os

st.set_page_config(
    page_title="Dashboard das notas do Enem nos últimos 5 anos",
    page_icon="📊",
    layout="centered",
    initial_sidebar_state="expanded"
)

st.title('Dashboard das notas do Enem nos últimos 5 anos 📊')

ano = st.selectbox('Escolha o ano para a análise:',
    ('2020', '2021', '2022', '2023', '2024'))

filtro = st.selectbox('Escolha uma variável para análise:',
                                    sorted(['Renda', 'Ano de conclusão', 'Raça']))

if filtro == 'Renda':
    salario = st.selectbox(
        'Escolha a faixa salarial:',
        ['Até R$1.420', 'Entre R$1.420 e R$3.530', 'Entre R$3.531 e R$9.884', 'Acima de R$9.884'])
