import httpx
import json
from app.utils.helpers import load_mock

KIWI_API_URL = "https://kiwi-com-cheap-flights.p.rapidapi.com/round-trip"
KIWI_API_KEY = "989a9ad1cfmshc5724b8f61db6b2p1152cbjsn41b8b3c2d2b4"

def search_transport(origin: str, destination: str, date_from: str, date_to: str = None):
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
    if date_to:
        params["dateTo"] = date_to
    try:
        response = httpx.get(KIWI_API_URL, headers=headers, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        # Write the API response to a file for debugging
        with open("kiwi_api_response.json", "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        results = []
        for item in data.get("itineraries", []):
            # Outbound segment
            outbound = item.get("outbound", {})
            inbound = item.get("inbound", {})
            # Outbound info
            from_city = outbound["sectorSegments"][0]["segment"]["source"]["station"]["city"]["name"]
            to_city = outbound["sectorSegments"][0]["segment"]["destination"]["station"]["city"]["name"]
            duration = outbound.get("duration", 0)
            # Price (use EUR if available)
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