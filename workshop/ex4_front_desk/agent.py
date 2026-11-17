from google.adk.agents import Agent, SequentialAgent

from .budget import enforce_budget, save_trip_details
from .tools import (
    get_hotel_details,
    get_local_notes,
    get_restaurants,
    get_transport,
    search_flights,
    search_hotels,
)

# The trip-planning team from Exercise 3. Nothing to change here.
local_insider = Agent(
    name="local_insider",
    model="gemini-3.5-flash-lite",
    description="Knows local closures, events, strikes and beach conditions.",
    instruction="""Find the destination in the traveller's message and call
get_local_notes for it. Reply with one short line per day.""",
    tools=[get_local_notes],
    output_key="local_notes",
)

planner_agent = Agent(
    name="planner_agent",
    model="gemini-3.5-flash-lite",
    description="Plans trips: flights, a hotel within budget, and a day-by-day plan.",
    instruction="""You are TripMate, a friendly travel assistant.
Use the tools to find flights and hotels, then suggest a trip
with a day-by-day plan. Stay within the traveller's budget.

Local notes for the trip dates:
{local_notes}

Never schedule anything the local notes say is closed or unsafe.""",
    tools=[search_flights, search_hotels, get_hotel_details, save_trip_details],
    after_tool_callback=enforce_budget,
)

# Exercise 3's root_agent, renamed. It now has a description, because the
# concierge reads descriptions to decide who to hand a question to.
trip_planner = SequentialAgent(
    name="trip_planner",
    description="Plans a complete trip: checks local notes, then finds flights "
    "and a hotel within budget and writes a day-by-day plan.",
    sub_agents=[local_insider, planner_agent],
)

# TODO 1 (level 1): create food_guide, an Agent with:
#   - name, model, and a description: "Recommends restaurants and food markets
#     at the destination."
#   - an instruction to recommend places to eat using get_restaurants, that
#     includes the local notes and budget from state:
#         Local notes: {local_notes?}
#         Total trip budget: {budget_eur?} euros for {nights?} nights.
#     and tells it to skip anything the local notes say is closed.
#   - tools: get_restaurants
# The ? in {local_notes?} means "empty if it isn't in state yet", instead of an error.

# TODO 2 (level 2): create getting_around the same way, with get_transport.
#   It should warn about strikes or closures in the local notes and offer
#   alternatives.

# TODO 3 (level 1): make root_agent the concierge, an Agent with:
#   - name: "concierge"
#   - an instruction: it's the front desk of TripMate. It greets travellers and
#     answers quick general questions itself (for example, simple phrases in the
#     local language), and hands trip planning, restaurant tips and transport
#     advice to the right specialist.
#   - sub_agents=[trip_planner, food_guide] (add getting_around for level 2)
root_agent = trip_planner
