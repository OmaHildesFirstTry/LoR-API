from flask import Flask, jsonify, request
import requests

app = Flask(__name__)

# OpenAPI Specification Route
@app.route("/openapi.json", methods=["GET"])
def openapi():
    return jsonify({
        "openapi": "3.1.0",
        "info": {
            "title": "Legends of Runeterra Card API",
            "version": "1.0.0",
            "description": "Fetches all LoR cards for deck building with pagination."
        },
        "servers": [
            {"url": "https://lor-api.onrender.com"}
        ],
        "paths": {
            "/lor/cards": {
                "get": {
                    "summary": "Fetch paginated Legends of Runeterra cards",
                    "operationId": "getLoRCards",
                    "parameters": [
                        {
                            "name": "page",
                            "in": "query",
                            "description": "Page number for pagination",
                            "required": False,
                            "schema": {"type": "integer", "default": 1}
                        },
                        {
                            "name": "per_page",
                            "in": "query",
                            "description": "Number of cards per page",
                            "required": False,
                            "schema": {"type": "integer", "default": 100}
                        }
                    ],
                    "responses": {
                        "200": {
                            "description": "A paginated list of LoR cards",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "object",
                                        "properties": {
                                            "page": {"type": "integer"},
                                            "total_pages": {"type": "integer"},
                                            "cards": {
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

# Fetch all cards with pagination
def fetch_lor_cards(page, per_page):
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

    # Implement pagination
    total_cards = len(all_cards)
    total_pages = (total_cards // per_page) + (1 if total_cards % per_page > 0 else 0)
    start_idx = (page - 1) * per_page
    end_idx = start_idx + per_page

    return {
        "page": page,
        "total_pages": total_pages,
        "cards": all_cards[start_idx:end_idx]
    }

@app.route("/lor/cards", methods=["GET"])
def get_cards():
    page = int(request.args.get("page", 1))
    per_page = int(request.args.get("per_page", 100))
    return jsonify(fetch_lor_cards(page, per_page))

@app.route("/")
def home():
    return "LoR API is running! Use /lor/cards?page=1&per_page=100 to get paginated card data."

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
