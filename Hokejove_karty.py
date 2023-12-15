import streamlit as st
import pandas as pd
from PIL import Image, ImageDraw, ImageFont
import requests
from io import BytesIO


@st.cache_data
def load_data():
    df = pd.read_csv("https://raw.githubusercontent.com/DenikSport/Hokejove_karty/main/Database.csv",encoding='iso-8859-2', sep=';')
    return df

def extract_stats(data, player_name):
    """
    Extract the statistics for a given player or goalie based on their position.

    Args:
    data (DataFrame): The dataset containing player statistics.
    player_name (str): The name of the player or goalie to extract statistics for.

    Returns:
    dict: A dictionary containing formatted statistics data.
    """
    # Filter the data for the selected player
    player_data = data[data['Jméno'] == player_name]

    if player_data.empty:
        return None, None

    position = player_data.iloc[0]['Pozice']

    if position.lower() == 'brankář':
        # Extract goalie statistics
        stats_data, category_values = extract_goalie_stats(data, player_name)
    else:
        # Extract player statistics
        stats_data, category_values = extract_player_stats(data, player_name)

    return stats_data, category_values


def extract_player_stats(data, player_name):
    """
    Extract the statistics for a given player and format it into the required structure.
    
    Args:
    data (DataFrame): The dataset containing player statistics.
    player_name (str): The name of the player to extract statistics for.

    Returns:
    dict: A dictionary containing formatted statistics data.
    """
    # Filter the data for the selected player
    player_data = data[data['Jméno'] == player_name]

    if player_data.empty:
        return None, None

    # Extracting data for each category
    off_data = [
        ["Vliv na spoluhráče do ofenzivy", player_data.iloc[0]['OFF IMPACT']],
        ["Produktivita", player_data.iloc[0]['POINT PRODUCTION']],
        ["Střelba", player_data.iloc[0]['SHOOTING']],
        ["Přihrávky", player_data.iloc[0]['PASSING']],
        ["Získané přesilovky", player_data.iloc[0]['PEN DRAWN']],
        ["Přesilovka", player_data.iloc[0]['PP']]
    ]

    tra_data = [
        ["Střelecká aktivita", player_data.iloc[0]['SHOT CONTRI']],
        ["Nebezpečný střelecký pokus ze slotu", player_data.iloc[0]['HD CHANCES']],
        ["Přihrávka do slotu na střelu", player_data.iloc[0]['HD ASSISTS']],
        ["Vstup do of. pásma s pukem na holi", player_data.iloc[0]['CARRIES']],
        ["Vstup do of. pásma přihrávkou", player_data.iloc[0]['ENTRY PASSES']],
        ["Úspěšný výstup z defenzivního pásma", player_data.iloc[0]['POSS EXITS']]
    ]

    deff_data = [
        ["Vliv na spoluhráče do defenzivy", player_data.iloc[0]['DEF IMPACT']],
        ["Zastavený útok před vlastní modrou čarou", player_data.iloc[0]['DENIALS']],
        ["Získané puky napadáním (pouze útočníci)", player_data.iloc[0]['RECOVERIES']],
        ["Obtížnost role", player_data.iloc[0]['ROLE DIFF']],
        ["Fauly", player_data.iloc[0]['PEN TAKEN']],
        ["Oslabení", player_data.iloc[0]['PK']]
    ]

    # Combining data into the required format
    stats_data = {
        "OFENZÍVA": off_data,
        "TRANZICE": tra_data,
        "DEFENZÍVA": deff_data
    }

    # Using category values from the dataset
    category_values = {
        "OFENZÍVA": player_data.iloc[0]['OFF'],
        "TRANZICE": player_data.iloc[0]['TRA'],
        "DEFENZÍVA": player_data.iloc[0]['DEF']
    }

    return stats_data, category_values

def extract_goalie_stats(data, player_name):
    """
    Extract the statistics for a given goalie and format it into the required structure.

    Args:
    data (DataFrame): The dataset containing player statistics.
    player_name (str): The name of the player (goalie) to extract statistics for.

    Returns:
    dict: A dictionary containing formatted statistics data for goalies.
    """
    # Filter the data for the selected player
    player_data = data[data['Jméno'] == player_name]

    if player_data.empty:
        return None, None

    # Extracting data for each category for a goalie
    off_data = [
        ["Chycené góly na očekávání", player_data.iloc[0]['OFF IMPACT']],
        ["Kontrola dorážek", player_data.iloc[0]['POINT PRODUCTION']],
        ["Vysoce nebezpečné střely", player_data.iloc[0]['SHOOTING']],
        ["Středně nebezpečné střely", player_data.iloc[0]['PASSING']],
        ["Nízko nebezpečné střely", player_data.iloc[0]['PEN DRAWN']]
    ]

    tra_data = [
        ["Chycené góly na očekávání", player_data.iloc[0]['SHOT CONTRI']],
        ["Kontrola dorážek", player_data.iloc[0]['HD CHANCES']],
        ["Vysoce nebezpečné střely", player_data.iloc[0]['HD ASSISTS']],
        ["Středně nebezpečné střely", player_data.iloc[0]['CARRIES']],
        ["Nízko nebezpečné střely", player_data.iloc[0]['ENTRY PASSES']]
    ]

    deff_data = [
        ["Chycené góly na očekávání", player_data.iloc[0]['DEF IMPACT']],
        ["Kontrola dorážek", player_data.iloc[0]['DENIALS']],
        ["Vysoce nebezpečné střely", player_data.iloc[0]['RECOVERIES']],
        ["Středně nebezpečné střely", player_data.iloc[0]['ROLE DIFF']],
        ["Nízko nebezpečné střely", player_data.iloc[0]['PEN TAKEN']]
    ]

    # Combining data into the required format
    stats_data = {
        "VŠECHNY SITUACE": off_data,
        "5 PROTI 5": tra_data,
        "OSLABENÍ": deff_data
    }

    # Using category values from the dataset for goalies
    category_values = {
        "VŠECHNY SITUACE": player_data.iloc[0]['OFF'],
        "5 PROTI 5": player_data.iloc[0]['TRA'],
        "OSLABENÍ": player_data.iloc[0]['DEF']
    }

    return stats_data, category_values

data = load_data() 
st.write(data)

player_list = pd.unique(data[['Jméno']].values.ravel())
selected_player = st.selectbox("Vyberte hráče", player_list, index=0)

# Zobrazte vybraného hráče
st.write(f"Vybraný hráč: {selected_player}")

# Získání a zobrazení statistik vybraného hráče
stats, category_scores = extract_stats(data, selected_player)
st.write(stats)
st.write(category_scores)
