from flask import Flask, jsonify
import requests

app = Flask(__name__)

# Homepage route (fixes the 404 error)
@app.route("/")
def home():
    return "Legends of Runeterra API is running! Use /lor/cards to get data."

# List of URLs for all Legends of Runeterra card sets
SET_URLS = [
    "https://dd.b.pvp.net/latest/set1/en_us/data/set1-en_us.json",
    "https://dd.b.pvp.net/latest/set2/en_us/data/set2-en_us.json",
    "https://dd.b.pvp.net/latest/set3/en_us/data/set3-en_us.json",
    "https://dd.b.pvp.net/latest/set4/en_us/data/set4-en_us.json",
    "https://dd.b.pvp.net/latest/set5/en_us/data/set5-en_us.json",
    "https://dd.b.pvp.net/latest/set6/en_us/data/set6-en_us.json",
    "https://dd.b.pvp.net/latest/set7/en_us/data/set7-en_us.json",
    "https://dd.b.pvp.net/latest/set8/en_us/data/set8-en_us.json",
    "https://dd.b.pvp.net/latest/set9/en_us/data/set9-en_us.json"
]

# Function to fetch all Legends of Runeterra cards
def fetch_lor_cards():
    all_cards = []
    for url in SET_URLS:
        response = requests.get(url)
        if response.status_code == 200:
            set_cards = response.json()
            all_cards.extend(set_cards)  # Add all cards from the set to our list
        else:
            print(f"Failed to fetch {url}")
    return all_cards

@app.route("/lor/cards", methods=["GET"])
def get_cards():
    return jsonify(fetch_lor_cards())

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
