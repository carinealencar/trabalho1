import streamlit as st
import pandas as pd
import os
import plotly.express as px
import json
import json
streamlit run principal.py

@st.cache_data
def load_geojson(path):
    # Certifique-se de que o arquivo 'municipios_ibge.geojson.json' está no mesmo diretório
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)
geojson_municipios = load_geojson('municipios_ibge.geojson.json')

# Ajuste estes caminhos e nomes de arquivos se necessário
FILE_PATHS = {
    '2020': 'ENEM_2020_FILTRADO_LIMPO.zip'
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

st.title("🗺️ Visualização de Mapa (Média das Notas por Município)")

ano_selecionado = st.selectbox(
    'Escolha o ano para visualizar o mapa:',
    ('2020', '2021', '2022', '2023')
)

# --- Carregamento e Preparação dos Dados ---
caminho_arquivo = FILE_PATHS[ano_selecionado]
df_enem = load_data(caminho_arquivo)

st.info(f"Carregando dados do ENEM {ano_selecionado}...")

# 1. Calcula a Média Geral (somente para quem fez todas as provas)
colunas_notas = ['NU_NOTA_CH', 'NU_NOTA_CN', 'NU_NOTA_MT', 'NU_NOTA_LC']
df_mapa = df_enem[df_enem[colunas_notas].notna().all(axis=1)].copy()

df_mapa['MEDIA_GERAL'] = df_mapa[colunas_notas].mean(axis=1)

# 2. Agrupa a Média por Código do Município (o código usado no GeoJSON)
# O código do IBGE (município) geralmente está na coluna 'CO_MUNICIPIO_RESIDENCIA'
df_media_municipio = (
    df_mapa.groupby('CO_MUNICIPIO_ESC')['MEDIA_GERAL']
    .mean()
    .reset_index()
    .rename(columns={'CO_MUNICIPIO_ESC': 'CODIGO_IBGE', 'MEDIA_GERAL': 'Média Geral ENEM'})
)

# Transforma o código do IBGE para string (Plotly precisa do formato correto)
df_media_municipio['CODIGO_IBGE'] = df_media_municipio['CODIGO_IBGE'].astype(str)

st.subheader(f"Média Geral do ENEM {ano_selecionado} por Município")

# 3. Cria o Mapa Choropleth com Plotly Express
if not df_media_municipio.empty and geojson_municipios:
    fig = px.choropleth(
        df_media_municipio,
        geojson=geojson_municipios,
        locations='CODIGO_IBGE',  # Coluna no DataFrame com o ID do município
        featureidkey="properties.codarea",  # Coluna no GeoJSON que corresponde ao ID
        color='Média Geral ENEM',           # A coluna usada para colorir o mapa
        hover_name='CODIGO_IBGE',         # Informação mostrada ao passar o mouse (pode ser ajustado)
        color_continuous_scale="Viridis",
        scope="south america",            # Foca na região do Brasil
        title=f'Média Geral do ENEM {ano_selecionado} por Município'
    )

    # Configurações para ajustar o mapa para o Brasil
    fig.update_geos(fitbounds="locations", visible=False)
    fig.update_layout(margin={"r":0,"t":50,"l":0,"b":0})

    st.plotly_chart(fig, use_container_width=True)

else:
    st.warning("Não foi possível gerar o mapa. Verifique se os dados e o GeoJSON foram carregados corretamente.")
