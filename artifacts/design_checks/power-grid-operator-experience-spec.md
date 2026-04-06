# Game Experience Spec: Power Grid Operator

### Game
Power Grid Operator

### Core fantasy
I am the operator keeping a city alive through the night. Neighborhoods are pulling power, storms are hitting lines, batteries are draining, and the grid must stay balanced.

### Core action
Solving algebraic equations to determine how much power to route to each district, then allocating limited sources to keep the lights on.

### Why this action should feel satisfying
The snap of solving the equation is only half the loop — the other half is choosing which district gets power when you can't power all of them. That allocation decision under scarcity is the satisfaction source. You're not just computing, you're triaging.

### Why the math is inseparable from the world
You cannot route power without solving the equation. "Downtown needs 18 MW, solar gives 5, battery gives x" — the player must compute x = 13 to know what to route. And then they must decide: do I send 13 to Downtown, or split it between Downtown and the hospital? The math determines what's possible; the allocation determines who survives.

### First 30 seconds
See the grid map. Districts glow softly. Demand bars fill. First district starts pulling — one source is obvious, the missing value is easy. Solve it, route it, watch the district light up. "I get it — I'm keeping these lights on."

### Mid-run feeling
Two districts degrading at once. One battery is low. The equation for Midtown is 2x + 3 = 15 — harder than the first. Solve it, route it, but Eastside is browning out. Tension between speed and accuracy.

### Mistake feeling
A district goes dark. Sirens. Citizens react ("Midtown lost power!"). The blackout counter ticks up. But it's recoverable — the district can be restored on the next surge if you solve fast enough.

### Success feeling
The grid glows green. "All districts powered." The shift timer stops, time bonus awarded. The city is alive because of you.

### End-of-session feeling
Shift summary: districts saved, blackouts caused, overloads avoided, best save streak, efficiency rating. The player knows exactly where they succeeded and where they lost districts.

### Source of delight
- Saving a district at the last second before blackout
- Cascading blackouts from one mistake (dramatic, memorable)
- Perfect shift with all districts lit and a big time bonus
- Chaining stabilizations across three districts in quick succession

### Source of tension
- Multiple districts degrading simultaneously
- Finite battery capacity that depletes over the shift
- Storm events that knock out a source mid-shift
- Overload risk if you send too much power
- Time-sensitive rerouting when a source fails

### Source of replay
- Different demand patterns each session
- Random storm events changing which sources are available
- Source failures requiring real-time rebalancing
- Optional efficiency challenges (minimize total power used)
- Variable district count and demand complexity per level

### Three memorable moments
1. A neighborhood is seconds from blackout and I solve the missing value just in time — lights flicker back on
2. A storm knocks out the solar array mid-shift and I rebalance the entire city using only batteries and wind
3. I finish with all districts lit, zero blackouts, and a 30-second time bonus

### Personality source
- District names with character (Midtown, Harbor District, University Quarter)
- Radio chatter from districts ("Midtown reporting brownout!", "Harbor stable, thank you!")
- Grid operator status strip ("Quiet grid" → "Demand surge in Midtown" → "Brownout risk" → "City holding steady")
- Storm warnings with personality ("Storm approaching from the west — brace for impact")

### What would make this game feel dead
- If every equation is independent (no allocation decision, just solve and done)
- If the grid map is just decoration and doesn't affect decisions
- If there's no visual reaction when districts lose or gain power
- If storms are just harder equations, not source failures that change the problem

### What would make this game feel cheap
- If any generator can power any district equally (allocation is trivial)
- If the player never has to choose between districts (enough power for everyone always)
- If the equations are disconnected from the grid state (random problems, not grid-based)

### Why this could be sticky
The strongest reason a player might want another run: "Last time I lost Midtown to the storm. This time I'm going to pre-route battery power before the storm hits." The combination of algebraic skill + allocation strategy + random events means each session teaches something new about grid management.

### Minimal proof of wonder
If the player describes a specific district they saved or lost by name — "I saved the hospital but lost Harbor District" — the game is not just functional, it's memorable.

### Build recommendation
**Build now.** The concept passes all pre-build checks. The core loop is a multi-step decision chain. The fantasy carries the math. The consequence design is strong. The main risk (spreadsheety feel) is manageable with strong visual feedback.

### Notes
Early math (L1-L5): one-step equations, missing addend/subtrahend, balancing totals.
Mid-game (L6-L12): two-step equations, combining sources, capacity constraints.
Late-game (L13+): inequalities, multi-district simultaneous allocation, storm recovery.
