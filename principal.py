import streamlit as st
import pandas as pd
import plotly.express as px
import json

# ===============================
# CONFIGURAÇÃO DA PÁGINA
# ===============================
st.set_page_config(
    page_title="Dashboard das notas do ENEM",
    page_icon="📊",
    layout="centered",
    initial_sidebar_state="expanded"
)

# ===============================
# ARQUIVOS
# ===============================
FILE_PATHS = {
    '2020': 'ENEM_2020_FILTRADO_LIMPO.zip',
    '2021': 'ENEM_2021_FILTRADO_LIMPO.zip',
    '2022': 'ENEM_2022_FILTRADO_LIMPO.zip',
    '2023': 'ENEM_2023_FILTRADO_LIMPO.zip'
}

# ===============================
# FUNÇÕES DE CARGA
# ===============================
@st.cache_data
def load_geojson(path):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

@st.cache_data
def load_data(path):
    return pd.read_csv(
        path,
        sep=';',
        encoding='latin1',
        compression='zip',
        low_memory=False
    )

geojson_municipios = load_geojson('municipios_ibge.geojson.json')

# ===============================
# INTERFACE
# ===============================
st.title('Dashboard das notas do ENEM')

ano = st.selectbox('Ano:', list(FILE_PATHS.keys()))
filtro = st.selectbox('Filtro:', ['Renda', 'Raça'])

# ===============================
# MAPAS DE FILTRO
# ===============================
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

if filtro == 'Renda':
    salario = st.selectbox('Faixa de renda:', list(m_renda.keys()))

if filtro == 'Raça':
    raca = st.selectbox('Raça:', list(m_raca.keys()))

# ===============================
# BOTÃO
# ===============================
if st.button("Gerar análise"):
    caminho_arquivo = FILE_PATHS[ano]

    # ===============================
    # BASE IMUTÁVEL
    # ===============================
    df_base = load_data(caminho_arquivo)

    # ===============================
    # APLICA FILTROS
    # ===============================
    df_filtrado = df_base.copy()

    if filtro == 'Renda':
        df_filtrado = df_filtrado[df_filtrado['Q006'].isin(m_renda[salario])]

    if filtro == 'Raça':
        df_filtrado = df_filtrado[df_filtrado['TP_COR_RACA'] == m_raca[raca]]

    st.write(f"Participantes após filtros: {len(df_filtrado)}")

    # ===============================
    # MAPA MUNICIPAL
    # ===============================
    st.markdown("### 🗺️ Mapa Municipal – Média Geral das Notas")

    possiveis_colunas_municipio = [
        'CO_MUNICIPIO_ESC',
        'CO_MUNICIPIO_RESIDENCIA',
        'CO_MUNICIPIO_PROVA'
    ]

    COLUNA_MUNICIPIO = next(
        (c for c in possiveis_colunas_municipio if c in df_filtrado.columns),
        None
    )

    if COLUNA_MUNICIPIO is None:
        st.error("Nenhuma coluna de município encontrada.")
        st.stop()

    df_mapa = df_filtrado[
        (df_filtrado['TP_PRESENCA_CH'] == 1) &
        (df_filtrado['TP_PRESENCA_CN'] == 1) &
        (df_filtrado['TP_PRESENCA_MT'] == 1) &
        (df_filtrado['TP_PRESENCA_LC'] == 1) &
        (df_filtrado[COLUNA_MUNICIPIO].notna())
    ].copy()

    if df_mapa.empty:
        st.warning("Sem dados suficientes para o mapa.")
        st.stop()

    df_mapa['MEDIA_GERAL'] = df_mapa[
        ['NU_NOTA_CH', 'NU_NOTA_CN', 'NU_NOTA_MT', 'NU_NOTA_LC']
    ].mean(axis=1)

    df_mapa[COLUNA_MUNICIPIO] = (
        df_mapa[COLUNA_MUNICIPIO]
        .astype(int)
        .astype(str)
        .str.zfill(7)
    )

    df_municipio_media = (
        df_mapa
        .groupby(COLUNA_MUNICIPIO, as_index=False)
        .agg(MEDIA_MUNICIPIO=('MEDIA_GERAL', 'mean'))
    )

    fig = px.choropleth_mapbox(
        df_municipio_media,
        geojson=geojson_municipios,
        locations=COLUNA_MUNICIPIO,
        featureidkey='properties.id',
        color='MEDIA_MUNICIPIO',
        color_continuous_scale='Turbo',
        mapbox_style='carto-positron',
        zoom=3,
        center={'lat': -14, 'lon': -52},
        opacity=0.75,
        height=650,
        labels={'MEDIA_MUNICIPIO': 'Média Geral ENEM'}
    )

    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})

    st.plotly_chart(fig, use_container_width=True)
