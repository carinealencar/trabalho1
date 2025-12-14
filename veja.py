import streamlit as st
import json

st.set_page_config(page_title="Inspeção GeoJSON", layout="centered")

st.title("Inspeção da Estrutura do GeoJSON")

@st.cache_data
def load_geojson(path):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

geojson_path = "municipios_ibge.geojson.json"

geojson_data = load_geojson(geojson_path)

# 1. Chaves principais do GeoJSON
st.subheader("Chaves principais do GeoJSON")
st.write(list(geojson_data.keys()))

# 2. Verifica se existe 'features'
if "features" not in geojson_data:
    st.error("O arquivo GeoJSON NÃO possui a chave 'features'.")
    st.stop()

# 3. Quantidade de features
st.subheader("Quantidade de features (municípios)")
st.write(len(geojson_data["features"]))

# 4. Estrutura de UMA feature (primeiro município)
st.subheader("Estrutura de uma feature (exemplo)")
feature_exemplo = geojson_data["features"][0]
st.json(feature_exemplo)

# 5. Propriedades disponíveis dentro de 'properties'
if "properties" in feature_exemplo:
    st.subheader("Variáveis disponíveis em properties")
    st.write(list(feature_exemplo["properties"].keys()))
else:
    st.error("Esta feature não possui a chave 'properties'.")
