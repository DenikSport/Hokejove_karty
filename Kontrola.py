import streamlit as st
import pandas as pd
from PIL import Image
import os


st.markdown("""
    <style>
    .stApp {
        background-color: #2a2a2c;
    }
    </style>
    """, unsafe_allow_html=True)

st.markdown("""
    <style>
    .stApp {
        background-color: #2a2a2c;
    }
    </style>
    """, unsafe_allow_html=True)

@st.cache(ttl=60*60)
def load_data():
    data_path = 'https://raw.githubusercontent.com/DenikSport/Hokejove_karty/main/List.csv'
    data = pd.read_csv(data_path, sep=";", dtype={'Jmeno': 'str', 'Tym': 'str', 'image_path': 'str'})
    # Oprava cesty k obrázkům
    data['image_path'] = data['image_path'].str.replace('/mount/src/hokejove_karty/', '', regex=False)
    return data

data = load_data()
# Vytvoření selectboxu pro kluby
kluby = ['Všechny kluby'] + sorted(data['Tym'].unique().tolist())
vybrany_klub = st.selectbox('Vyberte hráče', kluby, label_visibility="collapsed")

# Filtrování dat podle vybraného klubu
if vybrany_klub != 'Všechny kluby':
    data = data[data['Tym'] == vybrany_klub]

# Vytvoření seznamu hráčů na základě filtrovaných dat
player_list = pd.unique(data[['Jmeno']].values.ravel())

# Vytvoření selectboxu pro hráče
selected_player = st.selectbox("Vyberte Tým", player_list, label_visibility="collapsed")

# Získání dat pro vybraného hráče
player_data = data[data['Jmeno'] == selected_player].iloc[0]
# Zobrazení informací o hráči a jeho obrázku

# Načtení a zobrazení obrázku hráče
image_path = os.path.join('Karty', os.path.basename(player_data['image_path']))
image = Image.open(image_path)
st.image(image)
