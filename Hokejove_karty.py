import streamlit as st
import pandas as pd
from PIL import Image
import os

# Načtení nahráného CSV souboru
data = pd.read_csv('https://raw.githubusercontent.com/DenikSport/Hokejove_karty/main/List.csv')

st.write(data)
# Předpokládámdsfdsfe, že druhý sloupec s názvem klubu je již správně pojmenovaný jako "Nazev Tymu" ve vašem souboru
# Pokud ne, prosím, upravte název sloupce podle vašeho souboru

# Vytvoření selectboxu pro kluby
kluby = ['Všechny kluby'] + sorted(data['Tym'].unique().tolist())
vybrany_klub = st.selectbox('Vyberte klub:', kluby)

# Filtrování dat podle vybraného klubu
if vybrany_klub != 'Všechny kluby':
    data = data[data['Nazev Tymu'] == vybrany_klub]

# Vytvoření seznamu hráčů na základě filtrovaných dat
player_list = pd.unique(data[['Jméno']].values.ravel())

# Vytvoření selectboxu pro hráče
selected_player = st.selectbox("Vyberte hráče:", player_list)

# Získání dat pro vybraného hráče
player_data = data[data['Jméno'] == selected_player].iloc[0]

# Zobrazení informací o hráči a jeho obrázku
st.write(f"Jméno: {player_data['Jméno']}")
st.write(f"Tým: {player_data['Nazev Tymu']}")

# Načtení a zobrazení obrázku hráče
image_path = player_data['image_path']
if os.path.exists(image_path):
    image = Image.open(image_path)
    st.image(image, caption=player_data['Jméno'])
