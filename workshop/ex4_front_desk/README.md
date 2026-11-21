# Exercise 4 (capstone): The front desk

**Goal:** build a front desk for TripMate, like a hotel reception. A main agent, the **concierge**, greets the traveller, answers simple questions itself and passes everything else to the right helper:

- trip plans go to the **trip planner** (your agents from Exercise 3),
- restaurant questions go to the **food guide**,
- transport questions go to **getting around**.

Trip plans must still stay within budget and respect the local news.

**You'll learn:** how one agent can pass a question to another. You list the helpers in `sub_agents=[...]` and give each one a short `description` of what it does. The concierge reads those descriptions to decide who should answer, just like the AI reads a tool's docstring.

There are no TODOs this time. `agent.py` has an outline, and `CHEATSHEET.md` in the repo root has every pattern you need. If you get stuck, open [HINTS.md](HINTS.md).

## What to build

```
concierge  (root_agent: answers quick questions, routes the rest)
 ├─ trip_planner     the Ex 3 SequentialAgent + a description
 │    ├─ local_insider   → state["local_notes"]
 │    └─ planner_agent   + budget rule from budget.py
 ├─ food_guide       get_restaurants, reads {local_notes?} {budget_eur?} {nights?}
 └─ getting_around   (level 2) get_transport, reads {local_notes?}
```

| Agent | What it does |
|---|---|
| `trip_planner` | Plans the trip: local notes first, then flights, a hotel within budget and a day-by-day plan. |
| `food_guide` | Recommends places to eat. Skips anything closed and keeps prices sensible for the budget. |
| `getting_around` | Explains how to get around. Warns about strikes and closures and offers alternatives. |
| `concierge` | Greets travellers, answers simple questions itself, and hands off planning, food and transport. |

Give every specialist a clear `description`: that's what the concierge reads to decide who to call.

`tools.py` has all the tools you need and `budget.py` has the budget rule. When ready, restart `adk web workshop` and pick `ex4_front_desk`.

## Levels

- **Level 1:** `trip_planner`, `food_guide` and the `concierge`. Pass tests 1–4.
- **Level 2:** add `getting_around`. Pass test 5.
- **Extras:** a `budget_tracker` that answers "How much of my €600 is left?" with a Python tool, your own specialist (weather, packing list), or a guardrail from the cheat sheet.

## Acceptance tests

Run them in order, in one session. Use the **Traces** tab to see which agent answered.

| # | Traveller says | Answered by | Passes if |
|---|---|---|---|
| 1 | "Hi! What can you help me with?" | concierge | It introduces the specialists |
| 2 | The golden prompt | trip_planner | Within budget, avoids closures and red flags |
| 3 | "How do I say thank you in Catalan?" | concierge | "Gràcies!", no hand-off |
| 4 | "Where should we eat on day 5? Nothing fancy." | food_guide | Affordable, not the Boqueria (closed that day) |
| 5 | "How do we get around on day 4?" | getting_around | Mentions the metro strike, suggests bikes or walking |

Golden prompt:

> I'm flying from Amsterdam to Barcelona for 4 nights. My total budget is €600. I love the beach and I want to stay close by! Plan my trip with flights, a hotel and a day-by-day plan.

## Tips

- `{local_notes?}` with a `?` means "empty if not in state yet" instead of an error.
- No reply and no error in `adk web`? `root_agent` isn't defined yet.
- Wrong specialist answering? Improve the descriptions first.
- "Already has a parent" error? An agent can have only one parent, so list `trip_planner` in one place only.

Stuck? Open [HINTS.md](HINTS.md) first. The full answer is in `solutions/ex4_front_desk/agent.py`.
