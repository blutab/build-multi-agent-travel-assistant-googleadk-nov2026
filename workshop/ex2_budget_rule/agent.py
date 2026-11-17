from google.adk.agents import Agent
from google.adk.tools.tool_context import ToolContext

from .tools import search_flights, search_hotels

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

    # TODO: keep only the hotels whose price_per_night + fees_per_night
    # is at most max_per_night. For now, every hotel gets through.
    affordable = tool_response["hotels"]

    return {
        "status": "success",
        "hotels": affordable,
        "note": f"Only hotels up to €{max_per_night:.0f}/night incl. fees are shown.",
    }


root_agent = Agent(
    name="tripmate",
    model="gemini-3.5-flash-lite",
    instruction="""You are TripMate, a friendly travel assistant.
Use the tools to find flights and hotels, then suggest a trip
with a day-by-day plan. Stay within the traveller's budget.""",
    # TODO: add save_trip_details to the tools.
    tools=[search_flights, search_hotels],
    # TODO: attach the budget rule: after_tool_callback=enforce_budget
)
