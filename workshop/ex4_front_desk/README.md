# Exercise 4 (capstone): The front desk

**Goal:** build a concierge that greets the traveller and lets the model route each question to the right specialist, while trip planning keeps all its guarantees.

**New idea:** an `Agent` with `sub_agents=[...]` reads each sub-agent's `description` and hands the conversation to the best one. A description is to an agent what a docstring is to a tool.

**Time:** 14 minutes (9 to build, 5 for the acceptance tests)

## The brief

TripMate is growing. Travellers don't only want trip plans: they ask where to eat and how to get around. Build a concierge that greets them, answers quick questions itself and sends the rest to the right specialist. Trip planning must keep its guarantees from Exercises 2 and 3.

## Target

```
concierge        Agent with sub_agents: answers quick questions, routes the rest
├─ trip_planner      the Exercise 3 team, unchanged, plus a description
│   ├─ local_insider     writes state["local_notes"]
│   └─ planner_agent     budget rule from Exercise 2
├─ food_guide        get_restaurants, reads {local_notes?} and {budget_eur?}
└─ getting_around    (level 2) get_transport, reads {local_notes?}
```

## Build (9 min)

Your work is in `agent.py`. The Exercise 3 team is already there as `trip_planner`, and `tools.py` has `get_restaurants` and `get_transport`. `CHEATSHEET.md` in the repo root has every pattern from today.

- **Level 1 (everyone):** TODO 1 (`food_guide`) and TODO 3 (`concierge`). Passes tests 1–4.
- **Level 2:** TODO 2 (`getting_around`), added to the concierge's sub-agents. Passes test 5.
- **Level 3 (stretch, or take home):** a `budget_tracker` that answers "How much of my €600 is left?". Do the sums in a Python tool that reads state, not in the model.

Then restart `adk web workshop` and pick `ex4_front_desk`.

## Acceptance tests

Run them in order, in one session.

| # | Traveller says | Should be answered by | Passes if |
|---|---|---|---|
| 1 | "Hi! What can you help me with?" | concierge | It introduces the specialists |
| 2 | The golden prompt | trip_planner | Within budget, and avoids closures and red flags |
| 3 | "How do I say thank you in Catalan?" | concierge itself | "Gràcies!", with no hand-off and no new itinerary |
| 4 | "Where should we eat on day 5? Nothing fancy." | food_guide | Affordable, and not the Boqueria (closed that day) |
| 5 (level 2) | "How do we get around on day 4?" | getting_around | It mentions the metro strike and suggests bikes or walking |

Golden prompt:

> I'm flying from Amsterdam to Barcelona for 4 nights. My total budget is €600. I love the beach! Plan my trip with flights, a hotel and a day-by-day plan.

Use the **Traces** tab to see which agent answered each message.

## Tips

- `{local_notes?}` with a question mark means "empty if it isn't in state yet", instead of an error.
- If a question goes to the wrong specialist, improve the descriptions first. That's what the concierge reads.
- An agent can have only one parent, which is why Exercise 3's `root_agent` is now `trip_planner`.

## Discuss

- Where does the model have freedom now, and where does it have none?
- When would you use `sub_agents` routing, and when a `SequentialAgent`?

Stuck? Compare your work with `solutions/ex4_front_desk/agent.py`.
