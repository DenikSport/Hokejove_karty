import streamlit as st
import PIL
import pandas as pd

st.set_page_config(
    page_title="Landing",
    page_icon="⚽",
)

st.title("Vítejte v této aplikaci! ⚽")

@st.cache_data
def load_data():
    df = pd.read_csv("https://raw.githubusercontent.com/DenikSport/Hokejove_karty/main/Database.csv",encoding='iso-8859-2')
    return df

df = load_data() 
st.write(df)
