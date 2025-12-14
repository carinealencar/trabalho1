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
    '2020': 'ENEM_2020_FILTRADO_LIMPO.zip',
    '2021': 'ENEM_2021_FILTRADO_LIMPO.zip',
    '2022': 'ENEM_2022_FILTRADO_LIMPO.zip',
    '2023': 'ENEM_2023_FILTRADO_LIMPO.zip'
}

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
                      sorted(['Renda', 'Ano de conclusão', 'Raça']))

if filtro == 'Renda':
    salario = st.selectbox(
        'Escolha a faixa salarial:',
        ['Nenhuma renda', 'Até 1 salário mínimo', 'Entre 1 e 3 salários mínimos', 'Entre 3 e 6 salários mínimos', 'Acima de 6 salários mínimos'])

if filtro == 'Ano de conclusão':
    ano_c = st.selectbox(
        'Escolha o período do ano de conclusão:',
        ['Entre 2007 e 2012', 'Entre 2013 e 2018', 'Nos últimos anos'])

if filtro == 'Raça':
    raca = st.selectbox(
        'Escolha a raça a analisar:',
        ['Preto', 'Pardo', 'Branco', 'Indígena', 'Amarelo', 'Não informado'])

m_renda = {
    'Nenhuma renda': ['A'],
    'Até 1 salário mínimo': ['B'],
    'Entre 1 e 3 salários mínimos': ['C', 'D'],
    'Entre 3 e 6 salários mínimos': ['E', 'F', 'G'],
    'Acima de 6 salários mínimos': ['H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q']
}

m_conclusao = {
    'Entre 2007 e 2012': [12, 13, 14, 15],
    'Entre 2013 e 2018': [6, 7, 8, 9, 10, 11],
    'Nos últimos anos': [1, 2, 3, 4, 5]
}

m_raca = {
    'Branco': 1,
    'Preto': 2,
    'Pardo': 3,
    'Amarelo': 4,
    'Indígena': 5,
    'Não declarado': 0
}

botao = st.button('Exibir gráficos')

if botao:
    caminho_arquivo = FILE_PATHS[ano]
    df = load_data(caminho_arquivo)
    st.subheader(f"Resultados e Análise do ENEM {ano}")
    if filtro == 'Renda':
        df = df[df['Q006'].isin(m_renda[salario])]

    if filtro == 'Ano de conclusão':
        df = df[df['TP_ANO_CONCLUIU'].isin(m_conclusao[ano_c])]
    
    if filtro == 'Raça':
        df = df[df['TP_COR_RACA'] == m_raca[raca]]

    st.write(f"Total de participantes após filtros: {len(df)}")

    if len(df) == 0:
        st.warning("Nenhum dado encontrado para os filtros selecionados.")
        st.stop()


    #Placar ausentes, presentes, eliminados
    st.markdown("### 📋 Placar de Presença nas Provas")
    provas = {'Ciências Humanas': 'TP_PRESENCA_CH', 'Ciências da Natureza': 'TP_PRESENCA_CN', 'Matemática': 'TP_PRESENCA_MT', 'Linguagens': 'TP_PRESENCA_LC'}
    placar_data = {'Prova': [], 'Presentes': [], 'Ausentes': [], 'Eliminados': []}
    for prova, coluna in provas.items():
            contagem = df[coluna].value_counts().sort_index()
            placar_data['Prova'].append(prova)
            placar_data['Presentes'].append(contagem.get(1, 0))
            placar_data['Ausentes'].append(contagem.get(0, 0))
            placar_data['Eliminados'].append(contagem.get(2, 0))
    placar_df = pd.DataFrame(placar_data)    
    st.dataframe(placar_df, use_container_width=True)

    #Gráfico de media de nota por categoria
    st.markdown("### 📊 Média das Notas por Prova (somente presentes)")
    medias = {
        'Ciências Humanas': df.loc[df['TP_PRESENCA_CH'] == 1, 'NU_NOTA_CH'].mean(),
        'Ciências da Natureza': df.loc[df['TP_PRESENCA_CN'] == 1, 'NU_NOTA_CN'].mean(),
        'Matemática': df.loc[df['TP_PRESENCA_MT'] == 1, 'NU_NOTA_MT'].mean(),
        'Linguagens': df.loc[df['TP_PRESENCA_LC'] == 1, 'NU_NOTA_LC'].mean(),
        'Redação': df.loc[df['TP_PRESENCA_LC'] == 1, 'NU_NOTA_REDACAO'].mean()
    }    
    df_medias = (pd.DataFrame.from_dict(medias, orient='index', columns=['Média']).reset_index().rename(columns={'index': 'Prova'}))
    fig = px.bar(df_medias, x='Prova', y='Média', title='Média das Notas por Área')
    st.plotly_chart(fig, use_container_width=True)

