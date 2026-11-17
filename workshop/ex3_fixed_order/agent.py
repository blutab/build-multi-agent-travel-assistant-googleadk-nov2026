from google.adk.agents import Agent, SequentialAgent

from .budget import enforce_budget, save_trip_details
from .tools import get_local_notes, search_flights, search_hotels

# TODO 1: create local_insider, an Agent with:
#   - name: "local_insider"
#   - model: "gemini-3.5-flash-lite"
#   - description: "Knows local closures, events, strikes and beach conditions."
#   - instruction: find the destination in the traveller's message, call
#     get_local_notes for it, and reply with one short line per day
#   - tools: get_local_notes
#   - output_key="local_notes", which saves its reply into state

# This is TripMate from Exercise 2, now called planner_agent.
planner_agent = Agent(
    name="planner_agent",
    model="gemini-3.5-flash-lite",
    description="Plans trips: flights, a hotel within budget, and a day-by-day plan.",
    instruction="""You are TripMate, a friendly travel assistant.
Use the tools to find flights and hotels, then suggest a trip
with a day-by-day plan. Stay within the traveller's budget.""",
    # TODO 3 (do this after TODO 2): add the local notes to the instruction above:
    #   Local notes for the trip dates:
    #   {local_notes}
    #
    #   Never schedule anything the local notes say is closed or unsafe.
    # {local_notes} reads the reply local_insider saved into state.
    tools=[search_flights, search_hotels, save_trip_details],
    after_tool_callback=enforce_budget,
)

# TODO 2: make root_agent a SequentialAgent named "tripmate" that runs
# local_insider, then planner_agent:
#     SequentialAgent(name=..., sub_agents=[...])
root_agent = planner_agent
