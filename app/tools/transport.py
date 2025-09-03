import httpx
import json
from app.utils.helpers import load_mock

KIWI_API_URL = "https://kiwi-com-cheap-flights.p.rapidapi.com/round-trip"
KIWI_API_KEY = "989a9ad1cfmshc5724b8f61db6b2p1152cbjsn41b8b3c2d2b4"

def search_one_way(origin: str, destination: str, date_from: str):
    ONE_WAY_URL = "https://kiwi-com-cheap-flights.p.rapidapi.com/one-way"
    headers = {
        "x-rapidapi-host": "kiwi-com-cheap-flights.p.rapidapi.com",
        "x-rapidapi-key": KIWI_API_KEY,
    }
    params = {
        "source": f"Airport:{origin}",
        "destination": f"Airport:{destination}",
        "currency": "eur",
        "locale": "en",
        "adults": 1,
        "children": 0,
        "infants": 0,
        "handbags": 1,
        "holdbags": 0,
        "cabinClass": "ECONOMY",
        "sortBy": "QUALITY",
        "sortOrder": "ASCENDING",
        "dateFrom": date_from,
        "limit": 20,
    }
    try:
        print("One-way params:", params)
        response = httpx.get(ONE_WAY_URL, headers=headers, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        print(json.dumps(data, indent=2))
        with open("kiwi_api_response.json", "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        results = []
        # Try both "data" and "itineraries" keys for compatibility
        items = data.get("data") or data.get("itineraries") or []
        for item in items:
            # Adapt this block to match the structure of items in "itineraries"
            from_city = item.get("from_city") or item.get("sector", {}).get("sectorSegments", [{}])[0].get("segment", {}).get("source", {}).get("station", {}).get("city", {}).get("name")
            to_city = item.get("to_city") or item.get("sector", {}).get("sectorSegments", [{}])[-1].get("segment", {}).get("destination", {}).get("station", {}).get("city", {}).get("name")
            # --- FIX: Safely extract price ---
            price = 0
            if isinstance(item.get("price"), dict):
                price = float(item["price"].get("amount", 0))
            elif isinstance(item.get("priceEur"), dict):
                price = float(item["priceEur"].get("amount", 0))
            elif isinstance(item.get("price"), (int, float, str)):
                price = float(item.get("price", 0))
            duration = item.get("duration", 0) or item.get("sector", {}).get("duration", 0)
            results.append({
                "from_city": from_city,
                "to_city": to_city,
                "price": price,
                "duration": f"{int(duration)//3600}h{(int(duration)//60)%60}m",
                "type": "flight"
            })
        return results
    except Exception as e:
        print("API error:", e)
        return load_mock("flights.json")

def search_transport(origin: str, destination: str, date_from: str, date_to: str = None):
    if date_to:
        return search_round_trip(origin, destination, date_from, date_to)
    else:
        return search_one_way(origin, destination, date_from)

def search_round_trip(origin: str, destination: str, date_from: str, date_to: str):
    ROUND_TRIP_URL = "https://kiwi-com-cheap-flights.p.rapidapi.com/round-trip"
    headers = {
        "x-rapidapi-host": "kiwi-com-cheap-flights.p.rapidapi.com",
        "x-rapidapi-key": KIWI_API_KEY,
    }
    params = {
        "source": f"Airport:{origin}",
        "destination": f"Airport:{destination}",
        "currency": "eur",
        "locale": "en",
        "adults": 1,
        "children": 0,
        "infants": 0,
        "handbags": 1,
        "holdbags": 0,
        "cabinClass": "ECONOMY",
        "sortBy": "QUALITY",
        "sortOrder": "ASCENDING",
        "dateFrom": date_from,
        "dateTo": date_to,
        "limit": 20,
    }
    try:
        response = httpx.get(ROUND_TRIP_URL, headers=headers, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        with open("kiwi_api_response.json", "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        results = []
        for item in data.get("itineraries", []):
            outbound = item.get("outbound", {})
            segments = outbound.get("sectorSegments", [])
            if not segments:
                continue
            from_city = segments[0]["segment"]["source"]["station"]["city"]["name"]
            to_city = segments[0]["segment"]["destination"]["station"]["city"]["name"]
            duration = outbound.get("duration", 0)
            price = float(item.get("priceEur", {}).get("amount", item.get("price", {}).get("amount", 0)))
            results.append({
                "from_city": from_city,
                "to_city": to_city,
                "price": price,
                "duration": f"{duration//3600}h{(duration//60)%60}m",
                "type": "flight"
            })
        return results
    except Exception as e:
        print("API error:", e)
        return load_mock("flights.json")