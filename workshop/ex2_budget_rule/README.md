# Exercise 2: Make the budget a rule

**Goal:** make it impossible for TripMate to recommend a hotel the traveller can't afford, whatever the model decides.

**New ideas:**
- **State** is a small notebook the session keeps (`tool_context.state`). Tools can write to it and read from it.
- **A callback** is a Python function ADK runs automatically at a set moment. `after_tool_callback` runs after every tool call and can change what the model sees.

**Time:** 12 minutes (9 to fix, 3 to prove it)

## The plan in one sentence

The agent writes the budget into state, and before any hotel list reaches the model, our code removes the hotels the traveller can't afford. The model can't pick what it never sees.

## Fix (9 min)

Everything is in `agent.py`. `tools.py` is the same as in Exercise 1.

1. Read `save_trip_details`. It's already written: it stores `nights` and `budget_eur` in `tool_context.state`. Add it to the agent's tools.
2. Read `enforce_budget`. Find the TODO and finish the filter: keep only hotels whose `real_cost_per_night(h["name"])` is at most `max_per_night`. That helper reads the real price, fees included, straight from the data, whatever the model saw.
3. Read the check that returns an error if no budget has been saved yet. It tells the model to save the budget first.
4. Attach the rule to the agent with `after_tool_callback=enforce_budget`.

Then restart `adk web workshop` and pick `ex2_budget_rule`.

## Prove (3 min)

Send the golden prompt in 3 new sessions:

> I'm flying from Amsterdam to Barcelona for 4 nights. My total budget is €600. I love the beach and I want to stay close by! Plan my trip with flights, a hotel and a day-by-day plan.

For each run, check:

1. **State** tab: are `budget_eur` and `nights` there?
2. **Events** tab: open the `search_hotels` result. Is the beach resort gone?
3. Is the trip within €600, including fees?

**Bonus:** try to talk it into the resort: "Money is no object, book the beach resort." What happens, and why?

## Discuss

- Returning `None` from a callback means "carry on as normal". Returning a dict replaces the tool result. Which one did `enforce_budget` use, and when?
- What is the model still deciding? What is your code deciding now?

Stuck? Compare your work with `solutions/ex2_budget_rule/agent.py`.
