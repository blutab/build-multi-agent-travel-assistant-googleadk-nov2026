from google.adk.agents import Agent
from google.adk.tools.tool_context import ToolContext

from .tools import (
    get_hotel_details,
    real_cost_per_night,
    search_flights,
    search_hotels,
)

# Hotels may use at most 80% of the total budget, which leaves room for the flight.
HOTEL_SHARE = 0.8


def save_trip_details(nights: int, budget_eur: int, tool_context: ToolContext) -> dict:
    """Saves the trip length and total budget. Call this before searching for hotels.

    Args:
        nights: How many nights the traveller is staying.
        budget_eur: The traveller's total budget for the whole trip, in euros.
    """
    # TODO 1: save both values in state, the session's notebook:
    #     tool_context.state["nights"] = ...
    #     tool_context.state["budget_eur"] = ...
    return {"status": "saved"}


def enforce_budget(tool, args, tool_context, tool_response):
    """Runs after every tool call. Hides hotels the traveller can't afford
    from the search results.

    It checks the real cost from our data, not the prices the model saw.

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

    # TODO 2: keep only the hotels whose real_cost_per_night(h["name"])
    # is at most max_per_night. For now, every hotel gets through.
    affordable = tool_response["hotels"]

    # Add the real nightly cost, so the model's sums include the fees.
    affordable = [
        {**h, "real_cost_per_night": real_cost_per_night(h["name"])}
        for h in affordable
    ]

    return {
        "status": "success",
        "hotels": affordable,
        "note": f"Only hotels up to €{max_per_night:.0f}/night incl. fees are shown. "
        "Use real_cost_per_night for totals: it includes the fees.",
    }


# Level 2: the rule has a hole. Find it with the break-it prompts in the README,
# then close it inside enforce_budget.

# Level 3 (if you finish early): write flag_budget(tool, args, tool_context,
# tool_response). Instead of removing hotels, keep them all and add two fields
# to each one:
#     "real_cost_per_night": real_cost_per_night(h["name"])
#     "within_budget": True or False
# Then attach it instead of enforce_budget: after_tool_callback=flag_budget


root_agent = Agent(
    name="tripmate",
    model="gemini-3.5-flash-lite",
    instruction="""You are TripMate, a friendly travel assistant.
Use the tools to find flights and hotels, then suggest a trip
with a day-by-day plan. Stay within the traveller's budget.""",
    # TODO 3: add save_trip_details to the tools.
    tools=[search_flights, search_hotels, get_hotel_details],
    # TODO 4: attach the budget rule: after_tool_callback=enforce_budget
)
