"""The tools the agent can call. Nothing to change here."""

import json
from pathlib import Path

# All exercises share the mock data in the data/ folder at the repo root.
DATA_DIR = Path(__file__).resolve().parents[2] / "data"


def _load(name: str) -> dict:
    return json.loads((DATA_DIR / f"{name}.json").read_text(encoding="utf-8"))


FLIGHTS = _load("flights")
HOTELS = _load("hotels")
LOCAL_NOTES = _load("local_notes")


def search_flights(origin: str, destination: str) -> dict:
    """Finds return flights between two cities. Prices cover the round trip.

    Args:
        origin: The departure city, for example "Amsterdam".
        destination: The arrival city, for example "Barcelona".
    """
    routes = FLIGHTS.get(origin.strip().lower(), {})
    flights = routes.get(destination.strip().lower())
    if not flights:
        return {
            "status": "error",
            "message": f"No flights found from {origin} to {destination}.",
        }
    return {"status": "success", "flights": flights}


def search_hotels(city: str) -> dict:
    """Finds hotels in a city.

    Args:
        city: The city to search in, for example "Barcelona".
    """
    hotels = HOTELS.get(city.strip().lower())
    if not hotels:
        return {"status": "error", "message": f"No hotels found in {city}."}
    return {"status": "success", "hotels": hotels}


def get_local_notes(city: str) -> dict:
    """Gets local notes for the trip dates: closures, events, strikes and beach
    conditions, one note per day.

    Args:
        city: The destination city, for example "Barcelona".
    """
    notes = LOCAL_NOTES.get(city.strip().lower())
    if not notes:
        return {"status": "error", "message": f"No local notes for {city}."}
    return {"status": "success", "notes": notes}
