import httpx
from config.settings import FLIGHT_API_URL, FLIGHT_API_KEY
from app.utils.helpers import load_mock

def search_transport(origin: str, destination: str, date: str):
    headers = {
        "x-rapidapi-host": "sky-scrapper.p.rapidapi.com",
        "x-rapidapi-key": FLIGHT_API_KEY,
    }
    params = {
        "legs": f'[{{"destination":"{destination}","origin":"{origin}","date":"{date}"}}]',
        "adults": 1,
        "currency": "USD",
        "locale": "en-US",
        "market": "en-US",
        "cabinClass": "economy",
        "countryCode": "US"
    }
    try:
        response = httpx.get(
            FLIGHT_API_URL,
            headers=headers,
            params=params,
            timeout=10,
        )
        response.raise_for_status()
        return response.json()
    except Exception:
        return load_mock("flights.json")