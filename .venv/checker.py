import requests
from bs4 import BeautifulSoup
import pyexcel_ods

# Function to crawl the top 100 cards for a color
def get_top_100_cards(color):
    url = f"https://edhrec.com/top/{color.lower()}#cardlists"
    print(f"Downloading from the URL: {url}")
    response = requests.get(url)

    # Check if request is correct
    if response.status_code != 200:
        print(f"Fehler beim Abrufen der Seite: {response.status_code}")
        return []

    # Parse page of the page
    soup = BeautifulSoup(response.text, 'html.parser')

    # Search for cardnames
    card_names = []
    for card_tag in soup.find_all('span', class_='Card_name__Mpa7S'):
        card_name = card_tag.text.strip()
        card_names.append(card_name)
        if len(card_names) >= 100:  # Stop after 100 cards (otherwise later cards will also be added
            break

    return card_names

# Crawl all cards banned in oru challenge
def get_all_top_100_cards():
    colors = ['white', 'blue', 'black', 'red', 'green', 'colorless', 'multicolor']
    all_cards = {}

    for color in colors:
        print(f"Abrufen der Top 100 Karten für {color}...")
        all_cards[color] = get_top_100_cards(color)

    return all_cards

# Save all cards in dict to file
def save_all_cards_to_file(cards_dict, filename="all_700_top_cards.txt"):
    all_cards = []
    for cards in cards_dict.values():
        all_cards.extend(cards)

    with open(filename, "w") as file:
        for card in all_cards:
            file.write(card + "\n")

    print(f"Alle {len(all_cards)} Karten wurden in '{filename}' gespeichert.")


# Load all cards from the file
def load_cards_from_file(filename):
    with open(filename, "r") as file:
        cards = [line.strip() for line in file.readlines()]
    return cards


# Checks whether a card in the card list exists in the ods file
def check_cards_in_ods(cards_list, ods_file_path):
    # open ODS file
    data = pyexcel_ods.get_data(ods_file_path)
    sheet = list(data.values())[0]  # Use the first ods page

    # Search for col "Karte"
    header = sheet[0]
    try:
        card_column_index = header.index("Karte")
    except ValueError:
        print("Spalte 'Karte' nicht gefunden.")
        return []

    # Create a list with all cards from "Karten"
    cards_in_ods = [row[card_column_index] for row in sheet[1:] if len(row) > card_column_index]

    # Transform it to string
    cards_in_ods = [card.strip() for card in cards_in_ods]

    # Check which cards are i nthe list
    matching_cards = [card for card in cards_list if card in cards_in_ods]

    print(matching_cards)

    return matching_cards


######################################### Test
# Check and downlaod forbidden cards
# all_card_dict = get_all_top_100_cards()

# Save cards to file
# save_all_cards_to_file(all_card_dict)

# Check if cards are in ods file
card_list = load_cards_from_file("all_700_top_cards.txt")
check_cards_in_ods(card_list, "examplepath")
