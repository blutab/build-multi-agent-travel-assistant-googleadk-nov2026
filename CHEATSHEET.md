# ADK cheat sheet

Every pattern from today, with a snippet.

## An agent with tools (Exercise 1)

A tool is a plain Python function. The model reads its name, type hints and docstring. Pass the function itself, without brackets.

```python
from google.adk.agents import Agent

def search_hotels(city: str) -> dict:
    """Finds hotels in a city."""
    return {"status": "success", "hotels": [...]}

root_agent = Agent(
    name="tripmate",
    model="gemini-3.5-flash-lite",
    instruction="You are TripMate, a friendly travel assistant.",
    tools=[search_hotels],
)
```

`adk web` looks for a variable called `root_agent` in `agent.py`.

## State (Exercise 2)

State is a notebook the session keeps. Add a `tool_context` parameter to a tool to read or write it. ADK fills it in, and the model never sees it.

```python
from google.adk.tools.tool_context import ToolContext

def save_trip_details(nights: int, budget_eur: int, tool_context: ToolContext) -> dict:
    """Saves the trip length and total budget."""
    tool_context.state["budget_eur"] = budget_eur
    return {"status": "saved"}
```

## A callback (Exercise 2)

`after_tool_callback` runs after every tool call. Return `None` to keep the result, or a dict to replace what the model sees. The parameter names must be exactly these.

```python
def enforce_budget(tool, args, tool_context, tool_response):
    if tool.name != "search_hotels":
        return None
    ...
    return {"status": "success", "hotels": affordable}

root_agent = Agent(..., after_tool_callback=enforce_budget)
```

## A fixed order (Exercise 3)

`SequentialAgent` runs its sub-agents in order, every time. `output_key` saves an agent's reply into state, and `{key}` in another agent's instruction reads it.

```python
from google.adk.agents import SequentialAgent

local_insider = Agent(..., output_key="local_notes")
planner_agent = Agent(..., instruction="Local notes:\n{local_notes}")

root_agent = SequentialAgent(
    name="tripmate",
    sub_agents=[local_insider, planner_agent],
)
```

`{key}` raises an error if the key isn't in state yet. `{key?}` gives empty text instead.

## Routing (Exercise 4)

An `Agent` with `sub_agents` reads each sub-agent's `description` and hands the conversation to the best one. Control passes to that specialist; it doesn't come back like a tool result.

```python
food_guide = Agent(
    name="food_guide",
    description="Recommends restaurants and food markets at the destination.",
    ...
)

root_agent = Agent(
    name="concierge",
    instruction="Answer quick questions yourself. Hand the rest to a specialist.",
    sub_agents=[trip_planner, food_guide],
)
```

An agent can have only one parent.

## Which tool for which job?

| You need | Use |
|---|---|
| The model to call your code | A tool |
| A rule that must always hold | State + a callback |
| Steps that must happen in order | `SequentialAgent` |
| The model to pick a specialist | `sub_agents` on an `Agent` |

Let the model handle language, taste and judgement. Let code handle rules, money and order.
