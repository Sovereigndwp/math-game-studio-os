# Snack Line Shuffle

## Concept name
Snack Line Shuffle

## Status
Approved concept entering P1 normalization and repo placement. Preview build is deferred until P1 implementation is explicitly approved.

## Core concept summary
Snack Line Shuffle is a K to 2 math game where children read the snack trays each child is holding, solve a small addition or subtraction expression, and place the children in the correct order from most snacks to least snacks or least snacks to most snacks depending on the rule for that level.

The player is not deciding who deserves more. The player is a kitchen helper sorting the line so the server can portion correctly and quickly.

## Math skill practiced

### Corrected CCSS alignment
Primary standard confirmed: **CCSS.MATH.CONTENT.1.OA.C.6**

Add and subtract within 20, demonstrating fluency for addition and subtraction within 10. Use strategies such as counting on, making ten, decomposing, and related reasoning.

### Precise cognitive act
Students compute the total number of snacks on each child's tray using small addition or subtraction expressions, compare those totals, and order 3 to 6 children by magnitude.

### Secondary standard removed
**1.NBT.B.3** is not an alignment claim for this game. It is only a downstream conceptual beneficiary. Snack Line Shuffle does not teach place value comparison with tens and ones notation.

### Prerequisites
- K.CC.B.4
- K.CC.B.5
- K.CC.C.6
- K.OA.A.1
- K.OA.A.2
- early 1.OA.A.1 exposure

### Natural follow ons
- 1.OA.D.7
- 2.OA.B.2 if speed and strategy layers are later added
- conceptual support only for later number comparison work

### Grade band rule
Core K to 1 levels must stay:
- within 10
- mostly addition
- 3 to 4 children maximum

Mixed addition and subtraction within 20, 5 to 6 children, and positional constraints are **Grade 2 plus ceiling layers**, not core K to 1 content.

### Portfolio slot
Confirmed open.
No K to 2 conflict in the current portfolio.
Snack Line Shuffle is the first K to 2 member of the **Compare and Order** family and the first proof case for the canonical interaction type **sequence_and_order**.

### Fluency caution
Do not claim that Snack Line Shuffle alone delivers fluency under 1.OA.C.6. It provides repeated practice and consolidation context. A fluency claim would require speed and automaticity layers not yet built.

## Core fantasy
I am the kitchen helper who reads every tray and puts the kids in the right order so the server knows exactly how much to put on each plate without guessing.

## Core action
Each child arrives at the kitchen window holding a tray that shows a small addition or subtraction expression such as 3+2, 7-1, or 9+0. The player reads each tray, computes the total, and drag-and-drops the kids into the correct positions in a short line so the line runs from the largest snack total to the smallest, or from the smallest to the largest when the level says so.

## Serve mechanic

### Locked decision
**Option B is locked**

As each child is dropped into a slot, that slot immediately signals local consistency with neighboring slots through color only.

- neutral means there is not enough neighboring information yet
- green means this local adjacency is correctly ordered
- amber means this pair conflicts and needs to be reconsidered

The player must compute or compare to resolve an amber pair.
The system never displays computed totals.

When all slots are filled and all adjacencies are green or neutral, the **Serve** button activates as a cosmetic confirmation tap only. It triggers the serving animation but reveals no new information and cannot be used as a probe.

There is no global check-everything step.
The only diagnostic information is local adjacency color.

### Wrong placement feedback
Amber glow on the conflicting pair plus a short child voice line such as:
- "Hey, I think I should go before you!"
- "Are you sure?"

No totals are revealed.
No explicit correct order is given.

## Permanent design rule
At no point may a feedback or hint system display the computed total of a child's snacks or explicitly identify a correct or incorrect ordering unless the player has already placed that child and inferred the comparison using their own computation.

The game may highlight which pair is in conflict through an amber glow, but it must never surface the underlying numbers, inequality relation, or explicit who-goes-first as part of error feedback.

This rule applies from P1 through P5.

## Natural ceiling
6 child mixed addition and subtraction lines within 20 with positional constraints such as fixed anchors or middle-slot rules.
Beyond this, unknowns or multi-step expressions require a different UI model and likely a different mechanic.

## Closest existing game
- Bakery Rush internally, but low cognitive similarity because Bakery Rush is exact-sum composition and Snack Line Shuffle is compare and order
- Khan Academy Kids and Moose Math externally, but those are closer to single question response than a sequencing puzzle

## Interaction type
**sequence_and_order**

This concept is the first proof case for that canonical interaction type.

## Family
**Compare and Order**

Snack Line Shuffle is the first K to 2 member of this family.

## Depth potential
Medium to high.
Depth can increase through:
- larger line length
- larger totals
- mixed addition and subtraction
- ordering rule variants
- positional constraints

Ceiling is reached when the player can handle 6 child mixed addition and subtraction lines within 20 with positional constraints and no visual support.

## Delight Gate verdict
Conditional pass.

Conditions:
1. The ordering direction must be visually unambiguous for non-readers.
2. At least two thematic worlds should eventually exist by P2 to prevent sameness.

## AI critique summary
Snack Line Shuffle fills the widest portfolio gap at once:
- K to 2 grade band
- Compare and Order family

The fantasy maps cleanly to the skill. Without computing the small totals, the player has no reliable signal for where each child belongs in line.

The main risk is trial and error without genuine computation. The locked per-placement adjacency feedback, delayed and local only, addresses this better than a global Serve check would.
