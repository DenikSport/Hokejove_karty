import streamlit as st
import pandas as pd
from PIL import Image, ImageDraw, ImageFont
import requests
from io import BytesIO
import os

st.write("Ahoj")
fonts_directory = '/mount/src/hokejove_karty/Fonts'

# Kontrola, zda podsložka existuje
if os.path.exists(fonts_directory):
    st.write("Podsložka 'Fonts' existuje.")

    # Výpis souborů v podsložce
    files_in_fonts = os.listdir(fonts_directory)
    st.write("Soubory v podsložce 'Fonts':", files_in_fonts)
else:
    st.write("Podsložka 'Fonts' neexistuje.")

@st.cache_data
def load_data():
    df = pd.read_csv("https://raw.githubusercontent.com/DenikSport/Hokejove_karty/main/Database.csv",encoding='windows-1250', sep=';')
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
#st.write(data)

player_list = pd.unique(data[['Jméno']].values.ravel())
selected_player = st.selectbox("Vyberte hráče", player_list, index=0)

# Zobrazte vybraného hráče
st.write(f"Vybraný hráč: {selected_player}")

stats_data, category_scores = extract_stats(data, selected_player)
if stats_data is not None:
    st.write(stats_data)
    st.write(category_scores)

original_width, original_height = 650, 830
scale_factor = 10  # Faktor, kterým zvětšíme obrázek
width, height = original_width * scale_factor, original_height * scale_factor

# Vytvoření obrázku s vyšším rozlišením
image = Image.new('RGB', (width, height), color='#2a2a2c')
draw = ImageDraw.Draw(image)

font_title = ImageFont.truetype('/mount/src/hokejove_karty/Fonts/Poppins-Bold.ttf', 24 * scale_factor)
font_category = ImageFont.truetype('/mount/src/hokejove_karty/Fonts/Poppins-Bold.ttf', 28 * scale_factor)
font_statistic = ImageFont.truetype('/mount/src/hokejove_karty/Fonts/Poppins-Regular.ttf', 20 * scale_factor)
font_statistic_bold = ImageFont.truetype('/mount/src/hokejove_karty/Fonts/Poppins-Bold.ttf', 16 * scale_factor)
font_pie_value_bold = ImageFont.truetype('/mount/src/hokejove_karty/Fonts/Poppins-Bold.ttf', 22 * scale_factor)
font_value_bold = ImageFont.truetype('/mount/src/hokejove_karty/Fonts/Poppins-Bold.ttf', 22 * scale_factor)


def get_color(value):
    if value == "-":
        return "#AAAAAA"  # Neutrální šedá
    elif value <= 20:
        return "#CF1E1C"
    elif value <= 40:
        return "#DE726F"
    elif value <= 60:
        return "#E6E6E6"
    elif value <= 80:
        return "#6AE492"
    else:
        return "#09DC51"

def draw_thick_border(rect, thickness, draw_obj, color="black"):
    for i in range(thickness):
        draw_obj.rectangle([rect[0]+i, rect[1]+i, rect[2]-i, rect[3]-i], outline=color)



y_offset = 125 * scale_factor
category_title_height = 60 * scale_factor
bar_max_width = 125 * scale_factor
bar_height = 25 * scale_factor
bar_x_start = 450 * scale_factor
value_x_position = 600 * scale_factor  # Nastavení X pozice hodnoty
pie_outer_radius = 25 * scale_factor
pie_inner_radius = 20 * scale_factor


logo_padding = 160  * scale_factor

draw.rectangle([10 * scale_factor, 20 * scale_factor, 500*scale_factor, 90 * scale_factor], fill="#5d5758")
draw.text((140  * scale_factor, 25 * scale_factor), "Lukáš Sedlák", fill="white", font=font_title)
draw.text((140 * scale_factor, 55 * scale_factor), "HC Dynamo Pardubice", fill="white", font=font_statistic)

# Přidání "Počet zápasů:" a "Body:"
draw.text((50 * scale_factor, 90 * scale_factor), "Sezona: 2023/24", fill="white", font=font_statistic)
draw.text((170 * scale_factor, 90 * scale_factor), " | ", fill="white", font=font_statistic)
draw.text((190 * scale_factor, 90 * scale_factor), "Pozice: Brankář", fill="white", font=font_statistic)
draw.text((260 * scale_factor, 90 * scale_factor), " | ", fill="white", font=font_statistic)
draw.text((280 * scale_factor, 90 * scale_factor), "Věk: 30", fill="white", font=font_statistic)
draw.text((380 * scale_factor, 90 * scale_factor), " | ", fill="white", font=font_statistic)
draw.text((400 * scale_factor, 90 * scale_factor), "Zápasy: 15", fill="white", font=font_statistic)
draw.text((480 * scale_factor, 90 * scale_factor), " | ", fill="white", font=font_statistic)
draw.text((500 * scale_factor, 90 * scale_factor), "Body: 10", fill="white", font=font_statistic)


for category, stats in stats_data.items():
    start_y_offset = y_offset
    total_category_height = category_title_height + (len(stats) * (bar_height + 2 * scale_factor))

    category_center_y = start_y_offset + (total_category_height / 2)
    category_title_bbox = draw.textbbox((0, 0), category, font=font_category)

    # Vykreslení názvu kategorie s pozadím
    draw.rectangle([10 * scale_factor, y_offset, width - (10 * scale_factor), y_offset + category_title_height], fill="#2a2a2c")
    text_x = (width / 2) - (category_title_bbox[2] / 2)
    text_y = y_offset + ((category_title_height - category_title_bbox[3]) / 2)
    draw.text((text_x, text_y), category, fill="white", font=font_category)
    y_offset += category_title_height

    for index, (stat, value) in enumerate(stats):
        row_color = "#3b3839" if index % 2 == 0 else "#404040"
        draw.rectangle([10 * scale_factor, y_offset, width - (10 * scale_factor), y_offset + bar_height], fill=row_color)

        # Zarovnání textu názvu podkategorie
        stat_text_size = draw.textsize(stat, font=font_statistic)
        stat_text_x = 20 * scale_factor
        stat_text_y = y_offset
        draw.text((stat_text_x, stat_text_y), stat, fill="white", font=font_statistic)



        # Výpočet a vykreslení sloupce hodnoty
        bar_x_end = bar_x_start + (value / 100) * bar_max_width
        draw.rectangle([bar_x_start, y_offset, bar_x_end, y_offset + bar_height], fill=get_color(value))

        # Zarovnání textu číselné hodnoty
        value_text = f"{value}"
        value_text_size = font_value_bold.getsize(value_text)
        value_text_x = value_x_position - (value_text_size[0] / 2)
        value_text_y = y_offset + (bar_height - value_text_size[1]) / 2 -25
        draw.text((value_text_x, value_text_y), value_text, fill="white", font=font_value_bold)

        y_offset += bar_height + (4 * scale_factor)

    pie_offset_right = 175 * scale_factor  # Zvětšení odsazení od pravého okraje
    pie_center_x = width - pie_offset_right
    pie_center_y = start_y_offset + (category_title_height / 2)
    pie_center = (pie_center_x, pie_center_y)
    values = [category_values[category], 100 - category_values[category]]
    colors = [get_color(category_values[category]), "#e6e6e6"]

    draw.pieslice([pie_center[0] - pie_outer_radius, pie_center[1] - pie_outer_radius, pie_center[0] + pie_outer_radius, pie_center[1] + pie_outer_radius], start=-90, end=(-90 + (values[0] / 100) * 360), fill=colors[0])
    draw.pieslice([pie_center[0] - pie_outer_radius, pie_center[1] - pie_outer_radius, pie_center[0] + pie_outer_radius, pie_center[1] + pie_outer_radius], start=(-90 + (values[0] / 100) * 360), end=270, fill=colors[1])
    draw.pieslice([pie_center[0] - pie_inner_radius, pie_center[1] - pie_inner_radius, pie_center[0] + pie_inner_radius, pie_center[1] + pie_inner_radius], start=-90, end=270, fill="#2a2a2c")

    category_value_text = f"{category_values[category]}"
    category_value_text_size = font_value_bold.getsize(category_value_text)
    category_value_text_x = pie_center[0] - (category_value_text_size[0] / 2)
    category_value_text_y = pie_center[1] - (category_value_text_size[1] / 2)-25
    draw.text((category_value_text_x, category_value_text_y), category_value_text, fill="white", font=font_value_bold)


    # Ohraničení celé tabulky
    #draw.rectangle([10, start_y_offset, width-10, y_offset], outline="black", width=3)

# Zobrazení obrázku

# Display the image
from IPython.display import display
display(image)

