from flask import Flask, jsonify, request
import requests  # ✅ Ensure requests is imported

app = Flask(__name__)

# OpenAPI Specification Route
@app.route("/openapi.json", methods=["GET"])
def openapi():
    return jsonify({
        "openapi": "3.1.0",  # ✅ Updated to match OpenAI's requirement
        "info": {
            "title": "Legends of Runeterra Card API",
            "version": "1.0.0",
            "description": "Fetches all LoR cards for deck building."
        },
        "servers": [
            {"url": "https://lor-api.onrender.com"}
        ],
        "paths": {
            "/lor/cards": {
                "get": {
                    "summary": "Fetch all Legends of Runeterra cards",
                    "operationId": "getLoRCards",
                    "responses": {
                        "200": {
                            "description": "A list of LoR cards",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "array",
                                        "items": {
                                            "type": "object",
                                            "properties": {
                                                "name": {"type": "string"},
                                                "region": {"type": "string"},
                                                "cost": {"type": "integer"},
                                                "attack": {"type": "integer"},
                                                "health": {"type": "integer"},
                                                "text": {"type": "string"},
                                                "cardCode": {"type": "string"}
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
    })

# List of URLs for all LoR sets
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

# Fetch all cards with reduced data size
def fetch_lor_cards():
    all_cards = []
    for url in SET_URLS:
        response = requests.get(url)
        if response.status_code == 200:
            cards = response.json()
            for card in cards:
                all_cards.append({
                    "name": card.get("name", ""),
                    "region": card.get("regionRef", ""),
                    "cost": card.get("cost", 0),
                    "attack": card.get("attack", 0),
                    "health": card.get("health", 0),
                    "text": card.get("descriptionRaw", ""),
                    "cardCode": card.get("cardCode", "")
                })
        else:
            print(f"Failed to fetch {url}")

    return all_cards

@app.route("/")
def home():
    return "LoR API is running! Use /lor/cards to get data."

@app.route("/lor/cards", methods=["GET"])
def get_cards():
    return jsonify(fetch_lor_cards())

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
