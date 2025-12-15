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

if botao:
    caminho_arquivo = FILE_PATHS[ano]
    df = load_data(caminho_arquivo)
    coluna_municipio = ['CO_MUNICIPIO_ESC']
    st.subheader(f"Resultados e Análise do ENEM {ano}")
    
    if filtro == 'Renda':
        df = df[df['Q006'].isin(m_renda[salario])]
    if filtro == 'Raça':
        df = df[df['TP_COR_RACA'] == m_raca[raca]]

    st.write(f"Total de participantes após filtros: {len(df)}")

    if len(df) == 0:
        st.warning("Nenhum dado encontrado para os filtros selecionados.")
        st.stop()


    # Placar ausentes, presentes, eliminados
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

    # Gráfico de média de nota por categoria
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

    df_media = df.copy()

    df_media['MEDIA_GERAL'] = df_media[
        ['NU_NOTA_CH', 'NU_NOTA_CN', 'NU_NOTA_MT', 'NU_NOTA_LC']
    ].mean(axis=1)
    
    df_media = df_media.dropna(subset=['MEDIA_GERAL'])
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### 📦 Distribuição das Notas por Sexo")
        
        if not df_media.empty:
            fig_sexo = px.box(
                df_media,
                x='TP_SEXO',
                y='MEDIA_GERAL',
                labels={
                    'TP_SEXO': 'Sexo',
                    'MEDIA_GERAL': 'Nota Média'
                }
            )
            st.plotly_chart(fig_sexo, use_container_width=True)
        else:
             st.warning("Dados insuficientes para o gráfico de Notas por Sexo após remover NaNs.")

    with col2:
        st.markdown("### 📊 Média Geral das Notas por Faixa Etária")
        
        df_faixa = df[
                    (df['TP_PRESENCA_CH'] == 1) & (df['TP_PRESENCA_CN'] == 1) & (df['TP_PRESENCA_MT'] == 1) & (df['TP_PRESENCA_LC'] == 1) & (df['TP_FAIXA_ETARIA'].notna())
        ].copy()
        
        if not df_faixa.empty:
            df_faixa['Faixa Etária'] = df_faixa['TP_FAIXA_ETARIA'].map(m_faixa_etaria)
            df_faixa['MEDIA_GERAL'] = df_faixa[['NU_NOTA_CH', 'NU_NOTA_CN', 'NU_NOTA_MT', 'NU_NOTA_LC']].mean(axis=1)
            df_media_faixa = (df_faixa.groupby(['TP_FAIXA_ETARIA', 'Faixa Etária'])['MEDIA_GERAL'].mean().reset_index().sort_values('TP_FAIXA_ETARIA'))
                    
            fig_faixa = px.bar(
                df_media_faixa,
                x='MEDIA_GERAL',
                y='Faixa Etária', 
                orientation='h',
                labels={
                    'Faixa Etária': 'Faixa Etária',
                    'MEDIA_GERAL': 'Média Geral das Notas'
                }
            )
            st.plotly_chart(fig_faixa, use_container_width=True)
        else:
             st.warning("Dados insuficientes para o gráfico de Notas por Faixa Etária.")
            
    st.markdown("## 🗺️ Média Geral das Notas por Município")
    
    colunas_notas = [
        'NU_NOTA_CH',
        'NU_NOTA_CN',
        'NU_NOTA_MT',
        'NU_NOTA_LC',
        'NU_NOTA_REDACAO'
    ]
    
    coluna_municipio = 'CO_MUNICIPIO_ESC'
    
    df_mapa = df[
        (df['TP_PRESENCA_CH'] == 1) &
        (df['TP_PRESENCA_CN'] == 1) &
        (df['TP_PRESENCA_MT'] == 1) &
        (df['TP_PRESENCA_LC'] == 1) &
        (df[colunas_notas].notna().all(axis=1)) &
        (df[coluna_municipio].notna())
    ].copy()
    
    if df_mapa.empty:
        st.warning(
            f"Dados insuficientes para gerar o mapa de municípios do ENEM {ano} após os filtros."
        )
    else:
        df_mapa['MEDIA_GERAL'] = df_mapa[colunas_notas].mean(axis=1)
    
        df_municipio = (
            df_mapa
            .groupby(coluna_municipio, as_index=False)['MEDIA_GERAL']
            .mean()
        )
    
        df_municipio[coluna_municipio] = df_municipio[coluna_municipio].astype(str)
    
        fig_mapa = px.choropleth(
            df_municipio,
            geojson=geojson_municipios,
            locations=coluna_municipio,
            featureidkey='properties.id',
            color='MEDIA_GERAL',
            color_continuous_scale='Viridis',
            labels={'MEDIA_GERAL': 'Média Geral'},
            title=f'Média Geral das Notas do ENEM por Município — {ano}'
        )
    
        fig_mapa.update_geos(fitbounds="locations", visible=False)
        fig_mapa.update_layout(margin={"r": 0, "t": 50, "l": 0, "b": 0})
    
        st.plotly_chart(fig_mapa, use_container_width=True)
