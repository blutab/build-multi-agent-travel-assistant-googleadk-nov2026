"""The budget rule from Exercise 2. Nothing to change here."""

from google.adk.tools.tool_context import ToolContext

# Hotels may use at most 80% of the total budget, which leaves room for the flight.
HOTEL_SHARE = 0.8


def save_trip_details(nights: int, budget_eur: int, tool_context: ToolContext) -> dict:
    """Saves the trip length and total budget. Call this before searching for hotels.

    Args:
        nights: How many nights the traveller is staying.
        budget_eur: The traveller's total budget for the whole trip, in euros.
    """
    tool_context.state["nights"] = nights
    tool_context.state["budget_eur"] = budget_eur
    return {"status": "saved"}


def enforce_budget(tool, args, tool_context, tool_response):
    """Runs after every tool call. Hides hotels the traveller can't afford.

    Returning None keeps the tool's result as it is.
    Returning a dict replaces what the model sees.
    """
    if tool.name != "search_hotels" or tool_response.get("status") != "success":
        return None  # leave other tools, and errors, alone

    budget = tool_context.state.get("budget_eur")
    nights = tool_context.state.get("nights")
    if not budget or not nights:
        return {
            "status": "error",
            "message": "Ask for the budget and number of nights, "
            "then call save_trip_details.",
        }

    max_per_night = budget * HOTEL_SHARE / nights

    affordable = [
        h
        for h in tool_response["hotels"]
        if h["price_per_night"] + h["fees_per_night"] <= max_per_night
    ]

    return {
        "status": "success",
        "hotels": affordable,
        "note": f"Only hotels up to €{max_per_night:.0f}/night incl. fees are shown.",
    }
