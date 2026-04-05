from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

from utils.shared_agent_runner import AgentSpec, SharedAgentRunner


# ---------------------------------------------------------------------------
# Interaction-type misconception templates
# ---------------------------------------------------------------------------
# Each entry covers all six required error categories.
# Keys are the six category slugs; values are dicts with the 9 required fields
# already partially filled. The stub merges these with context-specific data
# from the briefs (e.g., failure state language, confusion risks).
# ---------------------------------------------------------------------------

_REQUIRED_FIELDS = {
    "id", "category", "label", "description", "likely_cause",
    "how_it_appears_in_play", "detection_signal",
    "best_feedback_response", "best_clean_replay_task", "reflection_prompt",
}

_SIX_CATEGORIES = [
    "impulsive_guess",
    "procedure_slip",
    "representation_mismatch",
    "concept_confusion",
    "rule_misunderstanding",
    "strategic_overload",
]

# Templates: one per interaction type × category.
# Format: (label, description_template, likely_cause, how_it_appears,
#           detection_signal, feedback, clean_replay, reflection_prompt)
# Placeholders: {family} = family_name slug, {domain} = math domain phrase

_TEMPLATES: Dict[str, Dict[str, Dict[str, str]]] = {

    "combine_and_build": {
        "impulsive_guess": {
            "label": "Tap before tracking",
            "description": "Learner taps items rapidly without computing a running total first. Treats the task as a reaction game rather than an arithmetic task.",
            "likely_cause": "Transfer from arcade games where speed is the primary skill. The moving belt signals urgency before it actually becomes urgent.",
            "how_it_appears_in_play": "Three or more consecutive taps under 500ms. Multiple overshoot events per order. No visible pause before the final item.",
            "detection_signal": "Three or more tap events within 1500ms total with at least one overshoot in the same order.",
            "best_feedback_response": "Stop and add. Your running total is X — how many more do you need before you tap again?",
            "best_clean_replay_task": "Belt frozen. Target ≤ 5. Only low-value items visible. Forced 1-second pause between taps. Success requires exact match.",
            "reflection_prompt": "Before you tapped, did you know how much you still needed? What would you check first next time?",
        },
        "procedure_slip": {
            "label": "Lost count near target",
            "description": "Learner is adding correctly but loses track of the running total on the final item — overshoots by 1 or 2 despite the correct strategy.",
            "likely_cause": "Working memory limit. Maintaining a running sum while scanning a moving belt exceeds current capacity, especially as targets grow.",
            "how_it_appears_in_play": "Correct strategy visible for first items. Overshoot happens on the last item only. Overshoot amount is small (1–3). Measured pace, not impulsive.",
            "detection_signal": "Overshoot on final tap only (total already ≥ target − 2 before the tap). Time between second-to-last and last tap > 1000ms.",
            "best_feedback_response": "You were at X — you only needed Y more. Check the running total before the last tap.",
            "best_clean_replay_task": "Belt frozen. Target ≤ 8. Running total shown with explicit 'need X more' label. Player confirms each item before it counts.",
            "reflection_prompt": "What was your running total right before you tapped the last item? Could you see it clearly?",
        },
        "representation_mismatch": {
            "label": "Icon not value",
            "description": "Learner selects items based on visual salience or icon preference rather than the numeric value label.",
            "likely_cause": "The icon is visually larger than the +N label. Learner has not yet connected the symbol to the quantity it represents.",
            "how_it_appears_in_play": "Consistent selection of one icon type regardless of value. Running total does not approach target predictably. Player seems surprised by overshoot.",
            "detection_signal": "Player selects the same icon type ≥ 70% of the time across 3+ orders. Overshoot rate > 40% compared to orders without preference pattern.",
            "best_feedback_response": "Every item has a number. Check the +N label before you tap — that is what gets added to your total.",
            "best_clean_replay_task": "All items same icon. +N label changes each round (1–5). Target ≤ 6. Player must match target using only the number, not the icon.",
            "reflection_prompt": "Which number on the belt mattered most for filling this order? How did you use it?",
        },
        "concept_confusion": {
            "label": "Count not sum",
            "description": "Learner believes the target means the number of items to add, not the sum of their values.",
            "likely_cause": "Without explicit instruction, 'give me 8 items' can mean '8 objects' in natural language. The value-weighting is the exact concept being taught.",
            "how_it_appears_in_play": "Player adds exactly N items where N = target, regardless of values. Running total does not match target. Player appears confused by failure.",
            "detection_signal": "Item count in box equals target number but running total does not match. Occurs on ≥ 2 consecutive orders.",
            "best_feedback_response": "The numbers need to add up to the target — not the count of items. A +4 and +4 makes 8 with just 2 items!",
            "best_clean_replay_task": "Two-item order only. Target = 8. Only +4 items available. Success when 4 + 4 = 8. Isolates sum-not-count with zero ambiguity.",
            "reflection_prompt": "What were the numbers on the items you picked? Did they add up to what was needed?",
        },
        "rule_misunderstanding": {
            "label": "Misreads failure feedback",
            "description": "After a game-mechanic correction (e.g. item returns after overshoot), learner stops playing or interprets the mechanic as a bug or full failure.",
            "likely_cause": "The corrective mechanic has no real-world analogy. Without a clear animation and feedback moment, it reads as a glitch or life loss.",
            "how_it_appears_in_play": "After correction feedback, player taps more items during the overlay window, or stops tapping and lets patience expire.",
            "detection_signal": "Tap event occurs during correction feedback window (within 700ms). Or order ends in timeout immediately after a correction event (0 subsequent taps).",
            "best_feedback_response": "One item automatically returns when you go over. Your total is now X — keep going!",
            "best_clean_replay_task": "Forced overshoot tutorial: target = 3. Only +4 items visible. Player must tap, see the return, then tap a +1 to correct. Three repetitions.",
            "reflection_prompt": "When the item returned, what was your total? What did you need to do next?",
        },
        "strategic_overload": {
            "label": "Freezes under combined pressure",
            "description": "Learner understands arithmetic and the belt mechanic separately, but cannot manage both simultaneously. Freezes or reverts to impulsive pattern under combined demand.",
            "likely_cause": "Cognitive load of tracking running total + scanning moving items + monitoring time simultaneously exceeds working memory capacity.",
            "how_it_appears_in_play": "Pause > 5 seconds mid-order with no taps. Rapid random tapping under pressure after previously controlled play. Performance degrades specifically at level transitions.",
            "detection_signal": "Order contains ≥ 5 second gap between taps without success. Or performance at new level ≥ 40% worse than previous level on first 3 orders.",
            "best_feedback_response": "Focus on the running total number first — ignore the belt for a moment. What number do you need to reach?",
            "best_clean_replay_task": "Static belt (no movement). Patience bar removed. Target ≤ 6. One pressure axis only. Player demonstrates arithmetic before pressure is reintroduced.",
            "reflection_prompt": "What made it harder this level? Was it the speed, the numbers, or trying to do both at once?",
        },
    },

    "route_and_dispatch": {
        "impulsive_guess": {
            "label": "Send without reading",
            "description": "Learner dispatches a resource without reading its capacity or properties. Treats the action as a sorting reflex rather than a constraint-matching decision.",
            "likely_cause": "Urgency cue (e.g. a timer or queue) triggers action before the learner has engaged the mathematical property. First available item is chosen, not the correct one.",
            "how_it_appears_in_play": "Player dispatches the first item in the list on every order regardless of capacity fit. No pause before selection. High rate of mismatches on first attempt.",
            "detection_signal": "Selection time < 600ms from order appearance on ≥ 3 consecutive dispatches. Mismatch rate > 50% on those orders.",
            "best_feedback_response": "Check the capacity number first. What is this order's requirement? Which resource matches it?",
            "best_clean_replay_task": "Single order. Two resources: one match, one mismatch by a factor of 2. Timer removed. Player must read both values before selecting.",
            "reflection_prompt": "Before you sent it, did you check whether the capacity matched? What would you look at first next time?",
        },
        "procedure_slip": {
            "label": "Off-by-one capacity",
            "description": "Learner knows which resource type is correct but selects one whose capacity is adjacent to (not equal to) the requirement.",
            "likely_cause": "Scanning multiple simultaneous values under time pressure creates substitution errors. Learner correctly identifies the category but reads the wrong number in that category.",
            "how_it_appears_in_play": "Correct resource type dispatched but wrong unit. Mismatch is always small (±1 or ±2). Pattern concentrated at higher difficulty levels with more resources on screen.",
            "detection_signal": "Dispatched resource capacity = requirement ± 1 or ± 2 on ≥ 3 orders. Error does not occur at low density (≤ 3 resources visible).",
            "best_feedback_response": "You picked the right type but the wrong amount. The order needs exactly X — which one on screen shows X?",
            "best_clean_replay_task": "All resources same type. Capacities: target ± 1, ± 2, and exact match. Player must identify exact match. No timer.",
            "reflection_prompt": "Did you read the number on the resource before you sent it, or did you go by the type?",
        },
        "representation_mismatch": {
            "label": "Icon not capacity",
            "description": "Learner selects a resource based on its icon or visual style rather than reading the capacity value that determines correctness.",
            "likely_cause": "Icon is more visually salient than the numeric label. Learner has automated a visual search pattern (find the matching icon) rather than a numerical comparison.",
            "how_it_appears_in_play": "Consistent selection of one icon type regardless of whether its capacity fits. Correct selections happen only when preferred icon also has correct capacity.",
            "detection_signal": "Player selects same icon type on ≥ 75% of dispatches. Mismatch rate for non-preferred icons is < 20%; mismatch rate for preferred icon is > 40%.",
            "best_feedback_response": "The icon type doesn't matter — the number does. What does this order need? Find that exact number on any resource.",
            "best_clean_replay_task": "All resources same icon. Capacity values vary (1×, 2×, 3×, 4× requirement). Player must select by number only.",
            "reflection_prompt": "Which number on the resource told you it was the right one to send?",
        },
        "concept_confusion": {
            "label": "Count not capacity",
            "description": "Learner believes the goal is to match the number of resources dispatched to the order size, not to match resource capacity to requirement.",
            "likely_cause": "Without the value-weighting frame, 'send 4 units' can mean '4 dispatches' in natural language. The capacity-matching mechanic is the exact concept being taught.",
            "how_it_appears_in_play": "Player sends exactly N resources where N = requirement number, regardless of capacity. Order fails but player appears confused.",
            "detection_signal": "Number of dispatched resources equals requirement number but total capacity does not meet requirement. Occurs on ≥ 2 consecutive orders.",
            "best_feedback_response": "You don't need to send 4 items — you need to send resources that add up to 4. One resource with capacity 4 works!",
            "best_clean_replay_task": "Requirement = 4. One resource available with capacity 4 and no other resources. Player must use one dispatch. Success teaches capacity = requirement.",
            "reflection_prompt": "How did you decide how many resources to send? What were the numbers you were matching?",
        },
        "rule_misunderstanding": {
            "label": "Reuses dispatched resource",
            "description": "Learner attempts to dispatch a resource that is already deployed, believing it can be reused within a round.",
            "likely_cause": "In everyday experience, tools and people can be reassigned. The 'single-use per round' rule is a game-mechanical constraint that has no obvious real-world analogy.",
            "how_it_appears_in_play": "Player taps a previously dispatched resource. Confused pause when the action is blocked. May repeat on the same resource multiple times.",
            "detection_signal": "Tap on a resource marked as dispatched (in-flight or deployed state) on ≥ 2 occasions within a session.",
            "best_feedback_response": "That resource is already deployed. You need a different one for this order.",
            "best_clean_replay_task": "Two identical resources. One already dispatched (grayed out). One available. Player must select the available one. Teaches single-use rule in isolation.",
            "reflection_prompt": "When you tried to send that one again, what happened? What does 'deployed' mean in this game?",
        },
        "strategic_overload": {
            "label": "Freezes on multi-attribute orders",
            "description": "Learner understands single-attribute matching but cannot dispatch when the order requires comparing two simultaneous attributes (e.g., capacity AND type).",
            "likely_cause": "Holding two comparison criteria in working memory simultaneously while scanning a resource pool exceeds capacity. Correct in isolation; fails under combined demands.",
            "how_it_appears_in_play": "Long pause (> 5s) on multi-attribute orders. Random dispatches. Correct performance on single-attribute orders in the same session.",
            "detection_signal": "Response time on multi-attribute orders > 3× response time on single-attribute orders in the same session. Or mismatch rate on multi-attribute orders > 2× single-attribute rate.",
            "best_feedback_response": "Focus on one number first. Does it meet the requirement? Then check the second condition.",
            "best_clean_replay_task": "One attribute only. Timer removed. Pool reduced to 3 resources. Player dispatches correctly, then a second attribute is introduced one step at a time.",
            "reflection_prompt": "What were the two things you needed to check? Which one did you look at first?",
        },
    },

    "navigate_and_position": {
        "impulsive_guess": {
            "label": "Place without checking",
            "description": "Learner places the target at a random position without first estimating or computing the correct location.",
            "likely_cause": "No habit of pre-placement reasoning. Learner treats placement as trial-and-error rather than as a derived position.",
            "how_it_appears_in_play": "Placement speed < 800ms from prompt appearance. Placement error > 30° or far from the correct position. Multiple rapid retries.",
            "detection_signal": "Placement within 800ms of prompt on ≥ 3 consecutive rounds. Error magnitude > 25% of the full range.",
            "best_feedback_response": "Before you place it, figure out where it should go. What do the reference labels tell you?",
            "best_clean_replay_task": "Single-axis placement. Only two reference points visible (0 and 90). Target is one of: 0, 45, 90. No timer.",
            "reflection_prompt": "Before you placed it, did you know where it should go? What did you use to figure that out?",
        },
        "procedure_slip": {
            "label": "Near miss at axis",
            "description": "Learner correctly identifies the quadrant and approximate angle but misses the exact position by a small margin — within tolerance on direction but not on precision.",
            "likely_cause": "Fine motor precision or visual estimation limit. Learner's conceptual understanding is correct but execution falls short of the required tolerance.",
            "how_it_appears_in_play": "Placement is in the correct half or quadrant. Error is small (< 10° or < 10% of range). Pattern is consistent across all attempts.",
            "detection_signal": "Placement error < precision threshold but direction is correct on ≥ 3 consecutive rounds. No directional reversal errors.",
            "best_feedback_response": "You're in the right area — just a bit off. The exact position is X. Try to land exactly on it.",
            "best_clean_replay_task": "Target snaps to nearest labeled reference point. Player must place on a labeled value only. No interpolation required. Builds exactness habit.",
            "reflection_prompt": "How close did you think you were before you placed it? What would help you hit it exactly?",
        },
        "representation_mismatch": {
            "label": "Degrees vs radians",
            "description": "Learner confuses degree and radian representations, placing at 90° when the target is π/2 or vice versa without understanding they name the same position.",
            "likely_cause": "Two systems taught separately. Learner has memorized isolated facts but has not built a connected model linking the two representations to a single position.",
            "how_it_appears_in_play": "Placement at 90° when radian target given. Or placement at π/2 ≈ 1.57 units along an arc when a degree target is given. Confusion concentrated on quadrant boundaries.",
            "detection_signal": "On radian-labeled tasks, placement within 5° of degree equivalent on ≥ 3 rounds (and vice versa). Confusion pattern symmetric between both directions.",
            "best_feedback_response": "90° and π/2 are the same point on the circle. They're two names for the same position.",
            "best_clean_replay_task": "Dual-label display: both degree and radian shown at same position. Player places at a labeled point and sees both labels light up simultaneously.",
            "reflection_prompt": "What is π/2 in degrees? How do you know they're the same place?",
        },
        "concept_confusion": {
            "label": "Clockwise confusion",
            "description": "Learner uses clockwise instead of counter-clockwise orientation (or vice versa), producing the mirror-image of the correct position.",
            "likely_cause": "Standard angle convention (counter-clockwise from positive x-axis) conflicts with clock reading and many everyday rotation references. The convention is arbitrary and easily reversed.",
            "how_it_appears_in_play": "Placement is at the correct angle magnitude but in the wrong rotational direction. Error is symmetric: target at 60° → placement at 300° (or equivalent).",
            "detection_signal": "Placement angle = 360° - target angle on ≥ 2 consecutive rounds. Error direction is always opposite, never random.",
            "best_feedback_response": "Angles go counter-clockwise from the right side of the circle. The 0° point is here — count upward from there.",
            "best_clean_replay_task": "Show only 0° and 90° with arrows indicating direction. Player places at 45°. Visual emphasis on which direction to count from.",
            "reflection_prompt": "Which direction did you count from? Which direction is positive for angles on this circle?",
        },
        "rule_misunderstanding": {
            "label": "Ignores tolerance ring",
            "description": "Learner places outside the acceptable tolerance zone repeatedly without understanding that the target has a precision requirement.",
            "likely_cause": "The tolerance ring or precision indicator is not salient enough. Learner believes any placement attempt counts as a valid try.",
            "how_it_appears_in_play": "Placements cluster near but outside the tolerance zone. Player does not adjust after feedback indicating 'too far'. Treats the feedback as random.",
            "detection_signal": "Placement error > tolerance threshold on ≥ 3 consecutive rounds despite receiving 'too far' feedback after each.",
            "best_feedback_response": "You need to land inside the shaded zone — that is the precision target. Aim for the center of the highlighted area.",
            "best_clean_replay_task": "Large tolerance zone (± 15°). Single target. Player places and sees the zone clearly. Zone narrows only after three consecutive successes.",
            "reflection_prompt": "Where is the target zone? Are you landing inside it or outside it?",
        },
        "strategic_overload": {
            "label": "Angle + quadrant overload",
            "description": "Learner can determine the angle magnitude or the quadrant separately but cannot combine both to produce a correct final placement when both must be resolved simultaneously.",
            "likely_cause": "Combining quadrant reasoning (positive/negative axes) with angle magnitude requires two simultaneous spatial transformations. Exceeds working memory for learners who have not automated either component.",
            "how_it_appears_in_play": "Correct in Quadrant I only. Random or wrong quadrant on II, III, IV targets despite correct magnitude range. Freezes or abandons placement under combined demand.",
            "detection_signal": "Accuracy on Quadrant I targets > 80%. Accuracy on Quadrant II–IV targets < 40% in the same session. Error pattern shows correct magnitude but wrong quadrant.",
            "best_feedback_response": "First: which quadrant? Then: how many degrees in from the axis? Do those two steps separately.",
            "best_clean_replay_task": "Quadrant I only. No angle values shown — only quadrant label. Player places anywhere in the correct quadrant first. Angle precision added only after quadrant is stable.",
            "reflection_prompt": "What did you figure out first — the direction or the exact angle? Which step was harder?",
        },
    },

    "allocate_and_balance": {
        "impulsive_guess": {
            "label": "Split without checking",
            "description": "Learner divides resources without verifying that both sides satisfy the constraint. Acts on first intuition rather than computing balance.",
            "likely_cause": "Visually-driven estimation habit. Learner splits 'in half' by appearance rather than computing exact equality.",
            "how_it_appears_in_play": "First allocation attempt is usually close but fails the equality check. Multiple rapid re-attempts without changing strategy.",
            "detection_signal": "First allocation attempt fails and time from task appearance to first attempt < 1000ms on ≥ 3 rounds.",
            "best_feedback_response": "Before splitting, figure out the total. Then ask: what is half of that?",
            "best_clean_replay_task": "Total = even number ≤ 10. Two equal bins. Player must state the target number for each bin before allocating. No timer.",
            "reflection_prompt": "Before you split it, did you know what number each side needed to reach?",
        },
        "procedure_slip": {
            "label": "Off-by-one distribution",
            "description": "Learner correctly computes the target for each side but places one unit in the wrong bin on the final allocation.",
            "likely_cause": "Fine motor error or counting slip on the last item, especially when the total is odd or the distribution involves three or more bins.",
            "how_it_appears_in_play": "Near-correct allocation on every attempt. Failure is always by 1. Pattern worsens with more bins or higher totals.",
            "detection_signal": "Difference between sides = 1 on ≥ 3 consecutive failed rounds. Player's strategy appears deliberate (not random).",
            "best_feedback_response": "One side has X, the other has Y — they need to match. Move one unit from the larger side.",
            "best_clean_replay_task": "Total = 6. Two bins. Target: 3 each. Only 7 moveable units (one extra). Player must find and leave out the extra.",
            "reflection_prompt": "Which side had more? How many did you need to move to make them equal?",
        },
        "representation_mismatch": {
            "label": "Value not piece count",
            "description": "Learner allocates by number of pieces rather than total value when pieces have different weights.",
            "likely_cause": "Treating all pieces as equal is the default — it is correct for uniform items. The weighted-value rule requires an extra layer of reasoning not yet automated.",
            "how_it_appears_in_play": "Equal number of pieces on each side but unequal total values. Player seems satisfied with equal counts.",
            "detection_signal": "Both sides have equal piece count but unequal value sum on ≥ 2 consecutive rounds.",
            "best_feedback_response": "Count the numbers, not the pieces. These items have different values — add them up on each side.",
            "best_clean_replay_task": "Two item types: value 1 and value 3. Total = 8. Four pieces total. Player must balance sums, not counts.",
            "reflection_prompt": "Did each side have the same total value, or just the same number of pieces?",
        },
        "concept_confusion": {
            "label": "Equal as same total, not same pieces",
            "description": "Learner does not understand that equality means equal sums, not identical contents. Believes sides must contain the same items to be equal.",
            "likely_cause": "Concrete equality (same things on both sides) precedes abstract equality (same value via different compositions). This is the core transition the game is teaching.",
            "how_it_appears_in_play": "Player copies items from one side to the other rather than achieving equal sums through different compositions. Rejects valid non-identical equal solutions.",
            "detection_signal": "Player repeatedly matches piece identities across bins (same items on both sides) even when different compositions would satisfy the constraint.",
            "best_feedback_response": "Equal doesn't mean the same items — it means the same total. 2 + 3 = 5 and 1 + 4 = 5 are both equal to 5.",
            "best_clean_replay_task": "Target = 5. Bin A has 2 + 3. Player must fill Bin B to equal 5 using only 1s and 4s. Shows non-identical equality.",
            "reflection_prompt": "Do both sides need the same pieces, or just the same total? What is equal actually measuring?",
        },
        "rule_misunderstanding": {
            "label": "Misreads constraint direction",
            "description": "Learner treats a minimum-threshold constraint as an exact-match constraint, stopping at the minimum rather than adjusting to achieve balance.",
            "likely_cause": "The game constraint language ('at least X' vs. 'exactly X') is subtle. Learner defaults to 'hit the target and stop' rather than reading the constraint type.",
            "how_it_appears_in_play": "Player fills one side to the minimum then stops, leaving the other side under the constraint. Appears satisfied with partial completion.",
            "detection_signal": "One bin at minimum threshold, other bin below threshold on ≥ 2 rounds. Player confirms despite imbalance.",
            "best_feedback_response": "Both sides need to satisfy the constraint — not just one. Check the other side too.",
            "best_clean_replay_task": "Two-bin task. Constraint: both sides must reach exactly 4. Player cannot confirm until both sides show 4. Rule made structurally explicit.",
            "reflection_prompt": "Does the rule apply to one side or both sides? How did you know when both conditions were met?",
        },
        "strategic_overload": {
            "label": "Freezes on three-bin balance",
            "description": "Learner can balance two bins but cannot manage three simultaneous constraints. Freezes or fails to adjust when a third condition appears.",
            "likely_cause": "Adding a third constraint triples the comparison space. Each adjustment now potentially breaks two other constraints. Exceeds planning capacity for learners not yet systematic.",
            "how_it_appears_in_play": "Correct on two-bin tasks. Freezes or randomly reassigns on three-bin tasks. Fixing one bin breaks another in a loop.",
            "detection_signal": "Two-bin accuracy > 80%. Three-bin accuracy < 40% in the same session. Reallocation count per three-bin task > 5 (thrashing pattern).",
            "best_feedback_response": "Work on one bin at a time. Fix the first bin completely, then move to the next.",
            "best_clean_replay_task": "Three bins but fix two in advance. Player adjusts only one bin. Teaches targeted adjustment before simultaneous balancing is introduced.",
            "reflection_prompt": "Which bin did you fix first? Did fixing it make the others easier or harder?",
        },
    },

    "sequence_and_predict": {
        "impulsive_guess": {
            "label": "Predict without pattern check",
            "description": "Learner submits a prediction before identifying the rule, substituting a guess or default value for the correct pattern continuation.",
            "likely_cause": "No habit of rule-extraction before answering. Learner treats prediction as recall rather than inference.",
            "how_it_appears_in_play": "Prediction submitted within 700ms. Answer equals first or last visible value. Pattern of guesses does not track visible sequence.",
            "detection_signal": "Prediction time < 700ms on ≥ 3 consecutive rounds. Prediction matches first or last term on ≥ 50% of attempts.",
            "best_feedback_response": "Find the rule before you predict. What changes between each step? By how much?",
            "best_clean_replay_task": "Sequence with visible difference labels (+2 between each term). Player must state the difference before predicting the next term.",
            "reflection_prompt": "What was the rule you found? How did you check it against the sequence?",
        },
        "procedure_slip": {
            "label": "One step off",
            "description": "Learner correctly identifies the rule but applies it to the wrong term — adds the difference to the wrong position in the sequence.",
            "likely_cause": "Counting or indexing error. Learner knows the rule but miscounts which term to extend from, especially with gaps or non-consecutive visible terms.",
            "how_it_appears_in_play": "Prediction = correct_answer ± rule_value. Error is always exactly one application of the rule. Correct on simple contiguous sequences.",
            "detection_signal": "Prediction = last_term + (2 × rule) or last_term (rule applied zero or twice). Error pattern is ± 1 rule-unit on ≥ 3 rounds.",
            "best_feedback_response": "Your rule is right, but apply it to the last number shown. What is that number plus your rule?",
            "best_clean_replay_task": "Sequence with explicit position labels (1st, 2nd, 3rd…). Player must tap the term they are extending from before submitting the prediction.",
            "reflection_prompt": "Which number did you add the rule to? Was that the last one in the sequence?",
        },
        "representation_mismatch": {
            "label": "Symbol not value",
            "description": "Learner cannot connect the symbolic representation (e.g., ×3, +5) to its effect on the sequence values, treating the symbol as a label rather than an operation.",
            "likely_cause": "Operation symbols have been drilled as notation but not fully connected to their numerical effects. Symbol-to-operation automation is incomplete.",
            "how_it_appears_in_play": "Learner correctly reads off the symbols but cannot produce the next term. May restate the rule but cannot apply it.",
            "detection_signal": "Correct rule identification (selects correct rule type) but incorrect prediction on ≥ 3 consecutive rounds.",
            "best_feedback_response": "The ×3 means multiply the last number by 3. Try it: what is 4 × 3?",
            "best_clean_replay_task": "Show operation as a number line step: arrow from 4 to 12 labeled '×3'. Player applies the same operation to a new starting number.",
            "reflection_prompt": "What does ×3 actually do to a number? Can you show it with a different starting number?",
        },
        "concept_confusion": {
            "label": "Repeating not growing",
            "description": "Learner applies a repeating-pattern model to a growing-pattern sequence, copying a fixed cycle rather than accumulating a difference.",
            "likely_cause": "Repeating patterns (ABAB) are learned earlier. Learner defaults to the cycle model when the sequence appears structured but does not recognize accumulation.",
            "how_it_appears_in_play": "Prediction matches an earlier term in the sequence (cycling back). Correct on repeating sequences in same session.",
            "detection_signal": "Prediction matches term at position (n − pattern_length) on ≥ 2 rounds. Correct predictions concentrated on repeating patterns only.",
            "best_feedback_response": "This sequence keeps getting bigger — it doesn't repeat. What changes between each step?",
            "best_clean_replay_task": "Side-by-side: one repeating (ABAB), one growing (+3). Player must label which type each is before predicting. Builds distinction.",
            "reflection_prompt": "Is this pattern repeating or growing? How do you tell the difference?",
        },
        "rule_misunderstanding": {
            "label": "Applies rule to all terms",
            "description": "Learner applies the rule to every visible term rather than only to the last term to predict the next, generating a set rather than the next element.",
            "likely_cause": "Misunderstanding of what is being asked. 'Continue the sequence' is parsed as 'apply the rule everywhere' rather than 'find what comes next'.",
            "how_it_appears_in_play": "Player submits multiple answers or selects all options. Or player states values for all positions rather than the next one.",
            "detection_signal": "Player selects more than one answer option on ≥ 2 consecutive prediction rounds. Or answer field contains multiple values.",
            "best_feedback_response": "You only need the next one. Cover the earlier terms and find what comes after the last number shown.",
            "best_clean_replay_task": "Show only the last term visible. Player predicts only the next one. Earlier terms hidden to focus the task.",
            "reflection_prompt": "What question were you answering — the whole pattern or just the next step?",
        },
        "strategic_overload": {
            "label": "Two-rule sequence overload",
            "description": "Learner can identify and apply one rule but cannot handle sequences governed by two simultaneous rules (e.g., alternating operations or compounding growth).",
            "likely_cause": "Two-rule sequences require holding both rules active and knowing which applies to each step. Exceeds working memory for learners who have not automated single-rule identification.",
            "how_it_appears_in_play": "Correct on single-rule sequences. Random or alternating errors on two-rule sequences. May identify both rules separately but cannot apply them in order.",
            "detection_signal": "Single-rule accuracy > 80%. Two-rule accuracy < 40% in the same session. Error pattern alternates (correct every other term).",
            "best_feedback_response": "This one has two rules — one for odd steps, one for even steps. Find each rule separately first.",
            "best_clean_replay_task": "Color-code even and odd steps. Player predicts even-step terms only first. Then odd-step only. Then combined.",
            "reflection_prompt": "Does the same rule apply to every step, or does it change? How many rules did you find?",
        },
    },

    "transform_and_manipulate": {
        "impulsive_guess": {
            "label": "Apply without reading input",
            "description": "Learner applies an operation without reading the current state of the object, producing a result based on a guessed or default input.",
            "likely_cause": "Habit of acting before reading. Learner treats the operation label as a complete instruction rather than requiring a current value to act on.",
            "how_it_appears_in_play": "Action within 800ms of operation prompt. Result is wrong but learner appears surprised. Rapid retry without re-reading.",
            "detection_signal": "Operation submitted < 800ms from prompt on ≥ 3 rounds. Incorrect on all fast-submit rounds.",
            "best_feedback_response": "Read the current value first. The operation changes that value — what is it right now?",
            "best_clean_replay_task": "No timer. Operation label hidden until player confirms they have read the current value. Forces read-before-act habit.",
            "reflection_prompt": "What was the starting value before you applied the operation? Did you check it first?",
        },
        "procedure_slip": {
            "label": "Wrong order of operations",
            "description": "Learner applies operations in the wrong order when two must be composed, producing the correct operations but in sequence-reversed order.",
            "likely_cause": "Order-of-operations rules are not yet internalized. Learner defaults to left-to-right order or applies the most recently seen operation first.",
            "how_it_appears_in_play": "Result is the value produced by the reverse operation order. Error is consistent — always the same reversal.",
            "detection_signal": "Result matches reverse-order application on ≥ 3 consecutive two-operation tasks.",
            "best_feedback_response": "Apply the first operation to the starting value, then apply the second to that result — not the other way around.",
            "best_clean_replay_task": "Two operations shown. Step 1 grayed out after completion. Step 2 activates only after. Forces sequential execution.",
            "reflection_prompt": "Which operation did you do first? What was the value in the middle, between the two steps?",
        },
        "representation_mismatch": {
            "label": "Symbol not action",
            "description": "Learner cannot connect the operation symbol to the physical transformation it represents, treating the symbol as decoration.",
            "likely_cause": "Symbol has been memorized as a label without being connected to a concrete action model. Learner can name the operation but cannot execute it.",
            "how_it_appears_in_play": "Learner correctly identifies the operation type but applies wrong transformation. e.g., reflects instead of rotates, or multiplies instead of scales.",
            "detection_signal": "Selects correct operation name but produces result matching a different operation ≥ 3 times.",
            "best_feedback_response": "This symbol means [operation]. Watch what it does: [animation]. Now you try it on this value.",
            "best_clean_replay_task": "Operation applied to a concrete manipulative (e.g., number line, shape). Player observes the transformation, then predicts result of same operation on new input.",
            "reflection_prompt": "What does this operation actually do to the number? Can you describe it without using the symbol name?",
        },
        "concept_confusion": {
            "label": "Confuses inverse and original",
            "description": "Learner does not recognize that applying an inverse operation returns the original value, treating the result as a new independent value.",
            "likely_cause": "Inverse relationship (undo concept) is not yet built into the learner's model of operations. Operations are seen as one-way transformations.",
            "how_it_appears_in_play": "After applying inverse, learner applies original operation again rather than verifying return to start. Does not recognize the loop.",
            "detection_signal": "After inverse application, learner immediately applies forward operation without checking result = original on ≥ 2 rounds.",
            "best_feedback_response": "Applying the inverse gets you back to where you started. What was the original value? Does your result match?",
            "best_clean_replay_task": "Start at 6. Apply ×2 → 12. Apply ÷2 → 6. Player must verify the return. Only two steps. Inverse relationship made explicit.",
            "reflection_prompt": "Where did you end up after the inverse? Is that where you started?",
        },
        "rule_misunderstanding": {
            "label": "Misreads operation scope",
            "description": "Learner applies an operation to the wrong element — e.g., applies a transformation to the whole expression rather than the targeted sub-element.",
            "likely_cause": "Scope of application (what the operation acts on) is not made explicit by the interface. Learner defaults to applying to the visible number rather than the designated target.",
            "how_it_appears_in_play": "Learner applies operation to a different element than intended. Result is wrong but internally consistent with their scope interpretation.",
            "detection_signal": "Result matches application to the non-targeted element on ≥ 3 consecutive rounds.",
            "best_feedback_response": "This operation acts only on the highlighted element. Which one is highlighted?",
            "best_clean_replay_task": "Only one element visible. Operation and target are unambiguous. Player completes successfully. Second element introduced only after rule is internalized.",
            "reflection_prompt": "Which element did you apply the operation to? How did you know it was the right one?",
        },
        "strategic_overload": {
            "label": "Chain overload",
            "description": "Learner can apply one transformation correctly but fails when three or more must be chained — losing track of the intermediate values.",
            "likely_cause": "Each transformation overwrites the intermediate state in working memory. Three-step chains require holding the output of each step long enough to use it as input for the next.",
            "how_it_appears_in_play": "Correct on single and double transforms. Random or early-step-recycled answers on triple chains. May correctly identify all operations but apply them to the starting value each time.",
            "detection_signal": "One-step accuracy > 90%. Three-step accuracy < 50% in the same session. Three-step results match applying all operations to initial value simultaneously.",
            "best_feedback_response": "After each step, write down (or remember) the new value before moving to the next operation.",
            "best_clean_replay_task": "Three-step chain with intermediate values shown after each step. Player confirms each intermediate before proceeding. External memory scaffold before internalization.",
            "reflection_prompt": "What was the value after the first step? After the second? Did you keep track of each one?",
        },
    },
}


# ---------------------------------------------------------------------------
# Utility helpers
# ---------------------------------------------------------------------------

def _infer_interaction_from_family(family_name: str) -> str:
    """Best-guess interaction type from family name when interaction_decision_memo
    is not available. Checks for known game names first, then keyword matches."""
    name = family_name.lower()
    if any(k in name for k in ("bakery", "combine", "build", "sum", "total")):
        return "combine_and_build"
    if any(k in name for k in ("fire", "dispatch", "route", "sort", "assign")):
        return "route_and_dispatch"
    if any(k in name for k in ("unit circle", "angle", "navigate", "position", "circle", "coordinate")):
        return "navigate_and_position"
    if any(k in name for k in ("balance", "equal", "allocate", "distribute")):
        return "allocate_and_balance"
    if any(k in name for k in ("pattern", "sequence", "predict", "series")):
        return "sequence_and_predict"
    if any(k in name for k in ("transform", "function", "operation", "algebra")):
        return "transform_and_manipulate"
    return "combine_and_build"  # safest default: most implemented family


def _load_library_entry(repo_root: Path, family_name: str, interaction_type: str) -> Optional[Dict]:
    """Load an existing misconception library entry for this game family, if present."""
    library_dir = repo_root / "artifacts" / "misconception_library"
    if not library_dir.is_dir():
        return None

    # Try exact game-name match first (slug-ified)
    slug = family_name.lower().replace(" ", "-").replace("_", "-")
    candidates = [
        library_dir / f"{slug}-misconceptions.json",
        library_dir / f"{slug}.json",
    ]
    # Also try interaction-type prefix
    candidates.append(library_dir / f"{interaction_type}-misconceptions.json")

    for path in candidates:
        if path.exists():
            try:
                with open(path) as f:
                    return json.load(f)
            except (json.JSONDecodeError, OSError):
                continue

    return None


def _all_fields_present(entry: Dict[str, Any]) -> bool:
    return _REQUIRED_FIELDS.issubset(entry.keys())


# ---------------------------------------------------------------------------
# Keyword-based category ↔ confusion-risk matching
# ---------------------------------------------------------------------------
# Maps each error category to keywords likely to appear in a brief's
# expected_confusion_risks list when that category is relevant.

_CATEGORY_KEYWORDS: Dict[str, List[str]] = {
    "impulsive_guess": ["tap before", "impuls", "before think", "without check", "rapid", "reflex", "sends all", "without reading", "tap-before"],
    "procedure_slip": ["lost count", "loses track", "loses count", "off-by-one", "arithmetic slip", "overshoot by 1"],
    "representation_mismatch": ["icon", "emoji", "preference", "visual", "label", "capacity icon", "not clearly read", "pastry icon"],
    "concept_confusion": ["item count", "number of items", "rather than sum", "count as capacity", "confused with item count", "count rather than"],
    "rule_misunderstanding": ["auto-correct", "mechanic", "misread as failure", "reuse", "reused", "believes used", "overshoot auto"],
    "strategic_overload": ["freeze", "combined", "pressure", "multi-constraint", "simultaneous", "overload", "both at once", "paralysis", "strategic"],
}


def _risk_matches_category(risk_text: str, category: str) -> bool:
    """Return True if a confusion-risk string is relevant to the given category."""
    risk_lower = risk_text.lower()
    for kw in _CATEGORY_KEYWORDS.get(category, []):
        if kw in risk_lower:
            return True
    return False


def _find_matching_risk(confusion_risks: List[str], category: str) -> Optional[str]:
    """Keyword fallback: return the first confusion-risk string that matches
    *category*, or None. Used when no LLM routing is available."""
    for risk in confusion_risks:
        if _risk_matches_category(risk, category):
            return risk
    return None


# ---------------------------------------------------------------------------
# Semantic risk routing — batch route all risks to categories via LLM
# ---------------------------------------------------------------------------

def _prompt_for_risk_routing(
    confusion_risks: List[str],
    categories: List[str],
    library_entries: Optional[Dict[str, Dict[str, str]]],
) -> str:
    """Build a prompt asking the model to route each brief risk to the best
    matching error category, or mark it as unmatched."""
    risks_block = "\n".join(
        f"  {i+1}. \"{r}\"" for i, r in enumerate(confusion_risks)
    )

    # Include library entry labels so the model can match risks to what exists
    cat_block_parts = []
    for cat in categories:
        lib_info = ""
        if library_entries and cat in library_entries:
            lib_info = f" — current entry: \"{library_entries[cat].get('label', 'N/A')}\""
        cat_block_parts.append(f"  - {cat}{lib_info}")
    cat_block = "\n".join(cat_block_parts)

    return _textwrap.dedent(f"""\
        You are a misconception analyst for a math learning game.

        Route each confusion risk from a game brief to the single best-matching
        error category. A risk should match a category if it describes the same
        kind of learner error — even if it uses different words.

        ## Error categories (with current library entry labels where available)
        {cat_block}

        ## Confusion risks from the brief
        {risks_block}

        ## Rules
        - Each risk maps to exactly ONE category, or "unmatched" if none fit.
        - A risk about a learner misunderstanding a game rule → rule_misunderstanding
        - A risk about cognitive overload from too many simultaneous demands → strategic_overload
        - A risk about confusing what a number represents → concept_confusion
        - A risk about visual/icon confusion → representation_mismatch
        - A risk about arithmetic errors or losing track → procedure_slip
        - A risk about acting before thinking → impulsive_guess
        - Only mark "unmatched" if the risk genuinely does not fit ANY category.

        Return a JSON object mapping each risk string (exactly as written above)
        to its category or "unmatched":
        {{
          "<risk text 1>": "<category_or_unmatched>",
          "<risk text 2>": "<category_or_unmatched>",
          ...
        }}

        Return ONLY the JSON object. No markdown fences, no other text.
    """)


def _route_risks_semantically(
    confusion_risks: List[str],
    categories: List[str],
    library_entries: Optional[Dict[str, Dict[str, str]]],
    gate_llm: Optional[Callable[[str], str]],
) -> Dict[str, str]:
    """Route brief risks to categories using semantic LLM comparison.

    Returns a dict mapping each risk string to a category name or "unmatched".
    Falls back to keyword matching if no LLM is available.
    """
    if not gate_llm or not confusion_risks:
        # Keyword fallback: build mapping from existing logic
        result: Dict[str, str] = {}
        for risk in confusion_risks:
            matched = False
            for cat in categories:
                if _risk_matches_category(risk, cat):
                    result[risk] = cat
                    matched = True
                    break
            if not matched:
                result[risk] = "unmatched"
        return result

    prompt = _prompt_for_risk_routing(confusion_risks, categories, library_entries)
    raw = _call_targeted_llm(gate_llm, prompt)

    if not raw or "_error" in raw:
        # LLM failed — fall back to keyword matching
        return _route_risks_semantically(
            confusion_risks, categories, library_entries, gate_llm=None,
        )

    # Validate the response: must map each risk to a known category or "unmatched"
    valid_targets = set(categories) | {"unmatched"}
    result = {}
    for risk in confusion_risks:
        assigned = raw.get(risk)
        if assigned in valid_targets:
            result[risk] = assigned
        else:
            # Model returned unknown key — try keyword fallback for this risk
            matched = False
            for cat in categories:
                if _risk_matches_category(risk, cat):
                    result[risk] = cat
                    matched = True
                    break
            if not matched:
                result[risk] = "unmatched"

    return result


def _find_matching_risk_from_routing(
    routing: Dict[str, str],
    category: str,
) -> Optional[str]:
    """Given a pre-computed routing map, find the first risk assigned to *category*."""
    for risk, assigned_cat in routing.items():
        if assigned_cat == category:
            return risk
    return None


def _risk_changes_entry_heuristic(risk_text: str, library_entry_fields: Dict[str, str]) -> bool:
    """Fast heuristic fallback: does the brief's confusion risk describe
    something the library entry does not already cover?

    Used when no LLM gate is available (deterministic-only mode).
    """
    risk_words = set(risk_text.lower().split())
    stop = {"the", "a", "an", "is", "are", "was", "were", "in", "on", "at",
            "to", "of", "and", "or", "not", "but", "for", "with", "by", "as",
            "that", "this", "it", "its", "be", "do", "does", "did", "has",
            "have", "had", "if", "than", "when", "from"}
    content_words = risk_words - stop
    if not content_words:
        return False

    haystack = " ".join([
        library_entry_fields.get("description", ""),
        library_entry_fields.get("how_it_appears_in_play", ""),
        library_entry_fields.get("detection_signal", ""),
        library_entry_fields.get("likely_cause", ""),
    ]).lower()

    missing = sum(1 for w in content_words if w not in haystack)
    return missing > len(content_words) / 2


def _prompt_for_risk_gate(
    risk_text: str,
    library_entry: Dict[str, str],
    category: str,
) -> str:
    """Build a focused prompt for the semantic revision gate.

    Asks the model a single yes/no question: does this brief risk introduce
    something the library entry does not already cover?
    """
    entry_summary = (
        f"Label: {library_entry.get('label', 'N/A')}\n"
        f"Description: {library_entry.get('description', 'N/A')}\n"
        f"Detection signal: {library_entry.get('detection_signal', 'N/A')}\n"
        f"How it appears in play: {library_entry.get('how_it_appears_in_play', 'N/A')}"
    )
    return _textwrap.dedent(f"""\
        You are a misconception analyst for a math learning game.

        An existing misconception library entry covers the "{category}" error category.

        ## Existing library entry
        {entry_summary}

        ## New confusion risk from the latest game brief
        "{risk_text}"

        ## Question
        Does the new confusion risk describe a meaningfully different or expanded
        concern that the existing library entry does NOT already cover?

        Answer with a JSON object:
        - "changes_entry": true or false
        - "reason": one sentence explaining your decision

        Return ONLY the JSON object. No other text.
    """)


def _risk_changes_entry(
    risk_text: str,
    library_entry_fields: Dict[str, str],
    category: str,
    gate_llm: Optional[Callable[[str], str]] = None,
) -> bool:
    """Determine whether a brief risk warrants revising a library entry.

    When gate_llm is provided, uses a lightweight semantic comparison.
    Otherwise falls back to the keyword heuristic.
    """
    if gate_llm is None:
        return _risk_changes_entry_heuristic(risk_text, library_entry_fields)

    prompt = _prompt_for_risk_gate(risk_text, library_entry_fields, category)
    result = _call_targeted_llm(gate_llm, prompt)
    if result and "_error" not in result:
        return bool(result.get("changes_entry", False))

    # LLM failed — fall back to heuristic
    return _risk_changes_entry_heuristic(risk_text, library_entry_fields)


def _diff_library_entry(
    library_entry: Optional[Dict],
    confusion_risks: List[str],
    interaction_type: str,
    family_name: str,
    gate_llm: Optional[Callable[[str], str]] = None,
    risk_routing: Optional[Dict[str, str]] = None,
) -> Dict[str, Dict[str, Any]]:
    """Diff seeded library entries against the current brief's confusion risks.

    Args:
        risk_routing: Pre-computed mapping of risk text -> category (or "unmatched").
                      When provided, used instead of _find_matching_risk.

    Returns a dict keyed by category, each value containing:
      - "action": "keep" | "revise" | "add"
      - "entry": the misconception dict (original, revised stub, or new stub)
      - "change_rationale": why this action was taken
      - "source": "library" | "template" | "stub"
    """
    results: Dict[str, Dict[str, Any]] = {}
    family_slug = family_name.lower().replace(" ", "_").replace("-", "_")

    if not library_entry:
        return results  # caller falls through to template/stub path

    lib_by_cat: Dict[str, Dict[str, Any]] = {}
    for m in library_entry.get("misconceptions", []):
        cat = m.get("category")
        if cat:
            lib_by_cat[cat] = m

    for category in _SIX_CATEGORIES:
        lib_m = lib_by_cat.get(category)
        if risk_routing:
            matching_risk = _find_matching_risk_from_routing(risk_routing, category)
        else:
            matching_risk = _find_matching_risk(confusion_risks, category)

        if lib_m is None:
            # Library has no entry for this category
            if matching_risk:
                results[category] = {
                    "action": "add",
                    "entry": None,  # caller will fill from template/stub
                    "change_rationale": (
                        f"No library entry for '{category}'. Brief confusion risk "
                        f"justifies adding: \"{matching_risk}\""
                    ),
                    "source": "pending",
                }
            else:
                results[category] = {
                    "action": "add",
                    "entry": None,
                    "change_rationale": (
                        f"No library entry for '{category}'. No direct brief risk "
                        f"either; filling from template for coverage."
                    ),
                    "source": "pending",
                }
            continue

        # Library entry exists for this category
        if not matching_risk:
            # Library entry exists but no brief risk matches this category.
            # Preserve it — the library has institutional knowledge we should keep.
            entry = dict(lib_m)
            entry["change_rationale"] = (
                f"Kept from library. No brief confusion risk directly targets "
                f"'{category}', but the misconception remains plausible for this "
                f"game mechanic."
            )
            results[category] = {
                "action": "keep",
                "entry": entry,
                "change_rationale": entry["change_rationale"],
                "source": "library",
            }
            continue

        # Both library entry and a matching brief risk exist.
        # Check if the brief risk introduces something the library entry
        # does not already cover.
        if _risk_changes_entry(matching_risk, lib_m, category, gate_llm):
            # The brief describes a changed or more specific risk.
            # Mark for revision — in stub mode we annotate what needs updating.
            entry = dict(lib_m)
            entry["change_rationale"] = (
                f"Revised: library entry existed but brief confusion risk "
                f"introduces changed context: \"{matching_risk}\". "
                f"Fields that may need LLM update: description, "
                f"how_it_appears_in_play, detection_signal."
            )
            # Tag fields that a real model should rewrite
            entry["_revision_needed"] = True
            entry["_revision_trigger"] = matching_risk
            results[category] = {
                "action": "revise",
                "entry": entry,
                "change_rationale": entry["change_rationale"],
                "source": "library-revised",
            }
        else:
            # Brief risk aligns with what the library already says — keep.
            entry = dict(lib_m)
            entry["change_rationale"] = (
                f"Kept from library. Brief confusion risk aligns with existing "
                f"entry: \"{matching_risk}\""
            )
            results[category] = {
                "action": "keep",
                "entry": entry,
                "change_rationale": entry["change_rationale"],
                "source": "library",
            }

    return results


def _build_misconception(
    interaction_type: str,
    category: str,
    family_name: str,
    confusion_risks: List[str],
    library_entry: Optional[Dict],
    diff_results: Optional[Dict[str, Dict[str, Any]]] = None,
) -> Dict[str, Any]:
    """Build one misconception entry for the given category.

    Priority:
    1. Use diff result if available (keep / revise / add from library diff).
    2. Use interaction-type template (with change_rationale).
    3. Fall back to minimal placeholder (stub mode).
    """
    family_slug = family_name.lower().replace(" ", "_").replace("-", "_")

    # --- Check diff results first (new path for known games) ---
    if diff_results and category in diff_results:
        dr = diff_results[category]
        if dr["entry"] is not None:
            # keep or revise — entry already populated
            return dr["entry"]
        # action == "add" with entry == None → fall through to template/stub

    # --- Legacy path: library without diff (should not happen after upgrade,
    #     but kept for safety) ---
    if library_entry and not diff_results:
        for lib_m in library_entry.get("misconceptions", []):
            if lib_m.get("category") == category:
                entry = dict(lib_m)
                entry["change_rationale"] = "Copied from library (legacy path — no diff performed)."
                return entry

    # --- Use template ---
    templates_for_type = _TEMPLATES.get(interaction_type, _TEMPLATES["combine_and_build"])
    tmpl = templates_for_type.get(category)

    rationale_prefix = ""
    if diff_results and category in diff_results:
        rationale_prefix = diff_results[category]["change_rationale"] + " "

    if tmpl:
        return {
            "id": f"{family_slug}_{category}",
            "category": category,
            "label": tmpl["label"],
            "description": tmpl["description"],
            "likely_cause": tmpl["likely_cause"],
            "how_it_appears_in_play": tmpl["how_it_appears_in_play"],
            "detection_signal": tmpl["detection_signal"],
            "best_feedback_response": tmpl["best_feedback_response"],
            "best_clean_replay_task": tmpl["best_clean_replay_task"],
            "reflection_prompt": tmpl["reflection_prompt"],
            "change_rationale": (
                rationale_prefix + "Filled from interaction-type template."
            ),
        }

    # Minimal fallback — stub mode; needs LLM to complete
    return {
        "id": f"{family_slug}_{category}",
        "category": category,
        "label": f"[STUB] {category} — complete with LLM run",
        "description": "Stub: requires LLM completion.",
        "likely_cause": "Stub: requires LLM completion.",
        "how_it_appears_in_play": "Stub: requires LLM completion.",
        "detection_signal": "Stub: requires LLM completion.",
        "best_feedback_response": "Stub: requires LLM completion.",
        "best_clean_replay_task": "Stub: requires LLM completion.",
        "reflection_prompt": "Stub: requires LLM completion.",
        "change_rationale": (
            rationale_prefix + "Stub: no library entry or template available."
        ),
    }


# ---------------------------------------------------------------------------
# Targeted LLM prompts — used only for revised entries and unmatched risks
# ---------------------------------------------------------------------------

import textwrap as _textwrap


def _prompt_for_revise_entry(
    library_entry: Dict[str, Any],
    new_risk: str,
    game_name: str,
    interaction_type: str,
    loop_brief_snippet: str,
) -> str:
    """Build a focused prompt asking the LLM to revise a single library entry
    given a changed confusion risk from the brief."""
    return _textwrap.dedent(f"""\
        You are the Misconception Architect for the Math Game Factory OS.

        A seeded misconception library entry exists for "{game_name}"
        (interaction type: {interaction_type}), but the latest game brief
        introduces a changed confusion risk that the entry does not fully cover.

        ## Current library entry
        ```json
        {json.dumps(library_entry, indent=2)}
        ```

        ## Changed confusion risk from the brief
        "{new_risk}"

        ## Relevant loop brief context
        {loop_brief_snippet}

        ## Your task
        Revise the library entry so it accurately reflects the changed risk.
        - Keep the same `id` and `category`.
        - Update `description`, `likely_cause`, `how_it_appears_in_play`,
          `detection_signal`, `best_feedback_response`, `best_clean_replay_task`,
          and `reflection_prompt` ONLY where the changed risk warrants it.
        - If a field still applies as-is, keep the original text.
        - Set `change_rationale` to a one-sentence explanation of what you changed and why.

        Return ONLY a single JSON object with all 10 required fields plus `change_rationale`.
        No markdown fences, no explanation outside the JSON.
    """)


def _prompt_for_unmatched_risk(
    risk_text: str,
    game_name: str,
    interaction_type: str,
    existing_categories: List[str],
    loop_brief_snippet: str,
) -> str:
    """Build a focused prompt asking the LLM to evaluate an unmatched brief risk
    and either produce a new misconception entry or reject it with rationale."""
    covered = ", ".join(existing_categories) if existing_categories else "(none)"
    family_slug = game_name.lower().replace(" ", "_").replace("-", "_")
    return _textwrap.dedent(f"""\
        You are the Misconception Architect for the Math Game Factory OS.

        A new confusion risk appeared in the latest brief for "{game_name}"
        (interaction type: {interaction_type}) that does not match any existing
        misconception entry.

        ## Unmatched confusion risk
        "{risk_text}"

        ## Categories already covered by existing entries
        {covered}

        ## Relevant loop brief context
        {loop_brief_snippet}

        ## Your task
        Decide: does this risk justify a new misconception entry?

        If YES:
        - Assign it to one of the six categories: procedure_slip, concept_confusion,
          representation_mismatch, impulsive_guess, rule_misunderstanding, strategic_overload.
        - If the best-fit category is already covered, you may still add a second entry
          for that category if the confusion is genuinely distinct.
        - Use id format: "{family_slug}_<descriptive_slug>"
        - Populate all 10 required fields: id, category, label, description, likely_cause,
          how_it_appears_in_play, detection_signal, best_feedback_response,
          best_clean_replay_task, reflection_prompt.
        - Set `change_rationale` explaining why a new entry is justified.
        - Return the JSON object.

        If NO (the risk is already covered by an existing entry, is too vague,
        or is not a learner misconception):
        - Return exactly: {{"rejected": true, "reason": "<one-sentence explanation>"}}

        Return ONLY the JSON object. No markdown fences, no text outside it.
    """)


def _call_targeted_llm(
    llm_callable: Callable[[str], str],
    prompt: str,
) -> Optional[Dict[str, Any]]:
    """Call the LLM with a focused prompt and parse the JSON response.

    Args:
        llm_callable: function(prompt_str) -> response_str
        prompt: the focused prompt text

    Returns:
        Parsed JSON dict, or None if parsing fails.
    """
    try:
        raw = llm_callable(prompt)
    except Exception as e:
        return {"_error": f"LLM call failed: {e}"}

    # Import the shared JSON extractor
    from utils.llm_caller import extract_json_from_text
    try:
        return extract_json_from_text(raw)
    except ValueError:
        return {"_error": f"Could not parse LLM response: {raw[:200]}"}


# ---------------------------------------------------------------------------
# Quality gate for model-produced entries
# ---------------------------------------------------------------------------

_GENERIC_REPLAY_MARKERS = [
    "try again", "repeat the level", "play again", "same level",
    "redo the task", "retry",
]


def _quality_check_revised(
    revised: Dict[str, Any],
    original: Dict[str, Any],
) -> Dict[str, Any]:
    """Validate a model-revised entry against quality criteria.

    Returns a dict with:
      - "passed": bool
      - "issues": list of issue strings (empty if passed)
      - "entry": the entry (possibly annotated with quality warnings)
    """
    issues: List[str] = []

    # 1. Detection signal must differ meaningfully from original
    orig_det = original.get("detection_signal", "").lower()
    new_det = revised.get("detection_signal", "").lower()
    if orig_det and new_det:
        # If the new signal is identical or a pure substring, flag it
        if new_det == orig_det:
            issues.append("detection_signal is identical to original — no revision occurred")
        elif len(new_det) < 20:
            issues.append("detection_signal is too short to be implementable")

    # 2. Clean replay task must be specific, not generic
    replay = revised.get("best_clean_replay_task", "").lower()
    for marker in _GENERIC_REPLAY_MARKERS:
        if marker in replay and len(replay) < 60:
            issues.append(f"clean_replay_task appears generic (contains '{marker}' with no specifics)")
            break

    # 3. Description must be non-trivially different from original
    orig_desc = original.get("description", "").lower()
    new_desc = revised.get("description", "").lower()
    if orig_desc and new_desc and orig_desc == new_desc:
        issues.append("description is identical to original — revision did not update it")

    if issues:
        revised["_quality_issues"] = issues

    return {
        "passed": len(issues) == 0,
        "issues": issues,
        "entry": revised,
    }


def _quality_check_new_entry(
    new_entry: Dict[str, Any],
    existing_entries: List[Dict[str, Any]],
) -> Dict[str, Any]:
    """Validate a model-added entry against quality criteria.

    Returns a dict with:
      - "passed": bool
      - "issues": list of issue strings
      - "entry": the entry (possibly annotated)
      - "near_duplicate_of": id of the near-duplicate entry, or None
    """
    issues: List[str] = []
    near_dup_id: Optional[str] = None

    new_cat = new_entry.get("category", "")
    new_desc = new_entry.get("description", "").lower()
    new_det = new_entry.get("detection_signal", "").lower()
    new_label = new_entry.get("label", "").lower()

    # 1. Check for near-duplicate against same-category entries
    for existing in existing_entries:
        if existing.get("category") != new_cat:
            continue
        ex_desc = existing.get("description", "").lower()
        ex_label = existing.get("label", "").lower()

        # Simple overlap check: if > 60% of words in the new description
        # appear in an existing same-category description, flag as near-dup
        new_words = set(new_desc.split()) - {"the", "a", "an", "is", "are",
            "to", "of", "and", "or", "not", "in", "on", "at", "for", "with"}
        if new_words:
            ex_words = set(ex_desc.split())
            overlap = len(new_words & ex_words) / len(new_words)
            if overlap > 0.6:
                near_dup_id = existing.get("id", "unknown")
                issues.append(
                    f"near-duplicate of '{near_dup_id}' in same category "
                    f"({new_cat}) — {overlap:.0%} description word overlap"
                )

        # Also check label similarity
        if new_label and ex_label and new_label == ex_label:
            issues.append(f"identical label to existing entry '{existing.get('id')}'")

    # 2. Clean replay must be specific
    replay = new_entry.get("best_clean_replay_task", "").lower()
    for marker in _GENERIC_REPLAY_MARKERS:
        if marker in replay and len(replay) < 60:
            issues.append(f"clean_replay_task appears generic (contains '{marker}')")
            break

    # 3. Detection signal must be non-trivial
    if len(new_det) < 20:
        issues.append("detection_signal is too short to be implementable")

    if issues:
        new_entry["_quality_issues"] = issues

    return {
        "passed": len(issues) == 0,
        "issues": issues,
        "entry": new_entry,
        "near_duplicate_of": near_dup_id,
    }


def _assign_category_priority(misconceptions: List[Dict[str, Any]]) -> None:
    """When multiple entries share a category, assign priority fields.

    The first entry for a category (from the library) gets priority "primary".
    Subsequent entries (from LLM additions) get priority "secondary" with a
    rationale linking back to the primary.
    """
    seen: Dict[str, str] = {}  # category -> id of primary entry
    for m in misconceptions:
        cat = m.get("category", "")
        if cat not in seen:
            seen[cat] = m.get("id", "unknown")
            m["priority"] = "primary"
        else:
            m["priority"] = "secondary"
            m["primary_entry_id"] = seen[cat]


# ---------------------------------------------------------------------------
# Quality gate retry
# ---------------------------------------------------------------------------

def _prompt_for_quality_retry(
    entry: Dict[str, Any],
    issues: List[str],
    context_type: str,  # "revised" or "new"
) -> str:
    """Build a prompt asking the model to fix specific quality issues."""
    issues_text = "\n".join(f"  - {issue}" for issue in issues)
    return _textwrap.dedent(f"""\
        You are the Misconception Architect for the Math Game Factory OS.

        You previously produced a {context_type} misconception entry, but it
        failed a quality check. Fix the specific issues listed below and return
        the corrected entry.

        ## Your previous entry
        ```json
        {json.dumps(entry, indent=2)}
        ```

        ## Quality issues to fix
        {issues_text}

        ## Rules
        - Fix ONLY the flagged issues. Do not change fields that passed.
        - Keep the same id and category.
        - detection_signal must be specific and implementable in-game.
        - best_clean_replay_task must describe a concrete, structurally different task
          (not "try again" or "repeat the level").
        - description must name the misunderstanding, not just the behavior.

        Return ONLY the corrected JSON object with all 10 required fields plus change_rationale.
        No markdown fences, no explanation outside the JSON.
    """)


def _retry_quality_check(
    entry: Dict[str, Any],
    issues: List[str],
    context_type: str,
    llm_callable: Callable[[str], str],
    original: Optional[Dict[str, Any]],
    existing_entries: Optional[List[Dict[str, Any]]],
) -> Dict[str, Any]:
    """Re-prompt the model once to fix quality issues.

    Returns a dict with:
      - "accepted": bool — whether the retried entry passed
      - "entry": the (possibly fixed) entry
      - "final_issues": remaining issues after retry (empty if accepted)
    """
    prompt = _prompt_for_quality_retry(entry, issues, context_type)
    result = _call_targeted_llm(llm_callable, prompt)

    if not result or "_error" in result or not _REQUIRED_FIELDS.issubset(result.keys()):
        return {"accepted": False, "entry": entry, "final_issues": issues}

    # Preserve id and category
    result["id"] = entry["id"]
    result["category"] = entry["category"]

    # Strip unexpected fields
    _allowed = _REQUIRED_FIELDS | {
        "change_rationale", "priority", "primary_entry_id", "quality_notes",
    }
    for k in list(result.keys()):
        if k not in _allowed:
            result.pop(k)

    # Re-check quality
    if context_type == "revised" and original:
        qc = _quality_check_revised(result, original)
    elif context_type == "new" and existing_entries is not None:
        qc = _quality_check_new_entry(result, existing_entries)
    else:
        qc = {"passed": True, "issues": []}

    if qc["passed"]:
        # Annotate that retry succeeded
        result["quality_notes"] = "Passed after 1 retry."
        return {"accepted": True, "entry": result, "final_issues": []}
    else:
        # Retry failed — keep original with issues annotated
        entry["quality_notes"] = (
            f"Failed quality check; retry also failed: {'; '.join(qc['issues'])}"
        )
        return {"accepted": False, "entry": entry, "final_issues": qc["issues"]}


# ---------------------------------------------------------------------------
# Main stub function
# ---------------------------------------------------------------------------

def misconception_architect_stub(
    context: Dict[str, Any],
    targeted_llm: Optional[Callable[[str], str]] = None,
    gate_llm: Optional[Callable[[str], str]] = None,
) -> Dict[str, Any]:
    """Deterministic stub for the Misconception Architect.

    Reads lowest_viable_loop_brief and family_architecture_brief (plus optional
    interaction_decision_memo). Cross-references artifacts/misconception_library/
    for known game families. Generates one misconception per error category.

    Model usage by tier:
      - gate_llm (cheap/fast): semantic keep-vs-revise decision for library entries.
        Falls back to keyword heuristic if not provided.
      - targeted_llm (strong): field-level rewrites for revised entries and
        category assignment + generation for unmatched risks.

    All other entries (kept from library, filled from template) remain deterministic.

    Gate threshold: valid_misconception_count >= 3.
    """
    loop_brief = context["artifact_inputs"]["lowest_viable_loop_brief"]
    family_brief = context["artifact_inputs"]["family_architecture_brief"]
    interaction_memo = context["artifact_inputs"].get("interaction_decision_memo", {})
    repo_root = Path(context.get("repo_root", "."))

    # --- Extract inputs ---
    family_name: str = family_brief.get("family_name", "unknown_family")
    interaction_type: str = (
        interaction_memo.get("primary_interaction_type")
        or _infer_interaction_from_family(family_name)
    )
    confusion_risks: List[str] = loop_brief.get("expected_confusion_risks", [])

    # Build a brief snippet for LLM context (first_60_seconds + fail state)
    loop_brief_snippet = (
        f"First 60 seconds: {loop_brief.get('first_60_seconds_flow', 'N/A')}\n"
        f"Fail state: {loop_brief.get('fail_state_structure', 'N/A')}\n"
        f"Loop description: {loop_brief.get('lowest_viable_loop_description', 'N/A')}"
    )

    # --- Cross-reference library ---
    library_entry = _load_library_entry(repo_root, family_name, interaction_type)
    library_used = library_entry is not None

    # --- Semantic risk routing (one batch call) ---
    # Route all brief risks to categories using haiku, or fall back to keywords.
    effective_gate = gate_llm or targeted_llm
    lib_by_cat_for_routing: Optional[Dict[str, Dict[str, str]]] = None
    if library_entry:
        lib_by_cat_for_routing = {}
        for m in library_entry.get("misconceptions", []):
            cat = m.get("category")
            if cat:
                lib_by_cat_for_routing[cat] = m

    risk_routing = _route_risks_semantically(
        confusion_risks, _SIX_CATEGORIES, lib_by_cat_for_routing, effective_gate,
    )

    # --- Diff-and-extend: compare library against current brief ---
    # Use gate_llm (cheap model) for keep-vs-revise decisions;
    # fall back to targeted_llm, then to keyword heuristic.
    diff_results = _diff_library_entry(
        library_entry, confusion_risks, interaction_type, family_name,
        gate_llm=effective_gate,
        risk_routing=risk_routing,
    )

    # --- Generate one entry per category ---
    misconceptions: List[Dict[str, Any]] = [
        _build_misconception(
            interaction_type, cat, family_name, confusion_risks,
            library_entry, diff_results if diff_results else None,
        )
        for cat in _SIX_CATEGORIES
    ]

    # --- Targeted LLM: revise entries and evaluate unmatched risks ---
    llm_revised_categories: List[str] = []
    llm_new_entries: List[Dict[str, Any]] = []
    llm_rejected_risks: List[Dict[str, str]] = []

    if targeted_llm and diff_results:
        # 1. Revise entries flagged by diff
        for i, m in enumerate(misconceptions):
            cat = m["category"]
            dr = diff_results.get(cat)
            if dr and dr["action"] == "revise":
                prompt = _prompt_for_revise_entry(
                    library_entry=m,
                    new_risk=dr.get("change_rationale", ""),
                    game_name=family_name,
                    interaction_type=interaction_type,
                    loop_brief_snippet=loop_brief_snippet,
                )
                result = _call_targeted_llm(targeted_llm, prompt)
                if result and "_error" not in result and "rejected" not in result:
                    # Validate that essential fields are present
                    if _REQUIRED_FIELDS.issubset(result.keys()):
                        # Preserve original id and category
                        result["id"] = m["id"]
                        result["category"] = cat
                        misconceptions[i] = result
                        llm_revised_categories.append(cat)

        # 2. Find unmatched risks using the pre-computed routing
        unmatched_risks = [
            risk for risk, assigned in risk_routing.items()
            if assigned == "unmatched"
        ]

        covered_cats = [m["category"] for m in misconceptions]
        for risk in unmatched_risks:
            prompt = _prompt_for_unmatched_risk(
                risk_text=risk,
                game_name=family_name,
                interaction_type=interaction_type,
                existing_categories=covered_cats,
                loop_brief_snippet=loop_brief_snippet,
            )
            result = _call_targeted_llm(targeted_llm, prompt)
            if result and "_error" not in result:
                if result.get("rejected"):
                    llm_rejected_risks.append({
                        "risk": risk,
                        "reason": result.get("reason", "no reason given"),
                    })
                elif _REQUIRED_FIELDS.issubset(result.keys()):
                    # Ensure change_rationale is present
                    if "change_rationale" not in result:
                        result["change_rationale"] = (
                            f"New entry added by LLM for unmatched risk: \"{risk}\""
                        )
                    llm_new_entries.append(result)
                    misconceptions.append(result)

    # --- Sanitize model output: strip fields not in schema ---
    _ALLOWED_FIELDS = _REQUIRED_FIELDS | {
        "change_rationale", "priority", "primary_entry_id", "quality_notes",
        "_revision_needed", "_revision_trigger", "_quality_issues",
    }
    for m in misconceptions:
        extra_keys = set(m.keys()) - _ALLOWED_FIELDS
        for k in extra_keys:
            m.pop(k)

    # --- Quality gate on model-produced entries (with one retry) ---
    quality_warnings: List[str] = []
    retries_fired = 0
    retries_accepted = 0

    if targeted_llm:
        # Check revised entries
        for i, m in enumerate(misconceptions):
            cat = m["category"]
            if cat in llm_revised_categories:
                dr = diff_results.get(cat)
                original = None
                if dr and library_entry:
                    for lib_m in library_entry.get("misconceptions", []):
                        if lib_m.get("category") == cat:
                            original = lib_m
                            break
                if original:
                    qc = _quality_check_revised(m, original)
                    if not qc["passed"]:
                        # Retry once
                        retries_fired += 1
                        retry = _retry_quality_check(
                            m, qc["issues"], "revised",
                            targeted_llm, original, None,
                        )
                        if retry["accepted"]:
                            misconceptions[i] = retry["entry"]
                            retries_accepted += 1
                        else:
                            warning = f"{cat}: {'; '.join(retry['final_issues'])}"
                            quality_warnings.append(warning)
                            misconceptions[i] = retry["entry"]

        # Check new entries
        base_entries = [m for m in misconceptions if m not in llm_new_entries]
        for j, new_entry in enumerate(llm_new_entries):
            qc = _quality_check_new_entry(new_entry, base_entries)
            if not qc["passed"]:
                # Retry once
                retries_fired += 1
                retry = _retry_quality_check(
                    new_entry, qc["issues"], "new",
                    targeted_llm, None, base_entries,
                )
                if retry["accepted"]:
                    # Replace in both llm_new_entries and misconceptions
                    idx = misconceptions.index(new_entry)
                    misconceptions[idx] = retry["entry"]
                    llm_new_entries[j] = retry["entry"]
                    retries_accepted += 1
                else:
                    warning = f"{new_entry.get('id', '?')}: {'; '.join(retry['final_issues'])}"
                    quality_warnings.append(warning)
                    idx = misconceptions.index(new_entry)
                    misconceptions[idx] = retry["entry"]

    # --- Assign category priority for duplicate categories ---
    _assign_category_priority(misconceptions)

    # --- Strip internal fields before validation ---
    for m in misconceptions:
        m.pop("_revision_needed", None)
        m.pop("_revision_trigger", None)
        m.pop("_quality_issues", None)

    # --- Gate check ---
    valid_count = sum(1 for m in misconceptions if _all_fields_present(m))
    gate_passed = valid_count >= 3
    status = "pass" if gate_passed else "revise"

    # --- Diff summary for notes ---
    if diff_results:
        actions = {a: [] for a in ("keep", "revise", "add")}
        for cat, dr in diff_results.items():
            actions[dr["action"]].append(cat)
        diff_summary = (
            f"Diff-and-extend: kept {len(actions['keep'])}, "
            f"revised {len(actions['revise'])}, "
            f"added {len(actions['add'])}. "
        )
    else:
        diff_summary = ""

    # --- LLM summary for notes ---
    llm_summary = ""
    if targeted_llm:
        parts = []
        if llm_revised_categories:
            parts.append(f"LLM revised {len(llm_revised_categories)} entries: {', '.join(llm_revised_categories)}")
        if llm_new_entries:
            parts.append(f"LLM added {len(llm_new_entries)} new entries")
        if llm_rejected_risks:
            reasons = "; ".join(f"\"{r['risk']}\": {r['reason']}" for r in llm_rejected_risks)
            parts.append(f"LLM rejected {len(llm_rejected_risks)} unmatched risks ({reasons})")
        if retries_fired > 0:
            parts.append(f"Quality gate retried {retries_fired}, accepted {retries_accepted}")
        if quality_warnings:
            parts.append(f"Quality gate flagged {len(quality_warnings)} remaining issues: {'; '.join(quality_warnings)}")
        if not parts:
            parts.append("LLM was available but no entries needed revision or addition")
        llm_summary = " ".join(parts) + ". "

    # --- Notes ---
    source_note = (
        f"Library entry found for '{family_name}'. {diff_summary}{llm_summary}"
        "Entries were diffed against brief confusion risks — not blindly copied."
        if library_used
        else f"No library entry found for '{family_name}'. "
             f"Interaction-type templates used (type: {interaction_type}). "
             "Run with a real model_callable to produce game-specific content."
    )
    confusion_note = (
        f"Confusion risks from loop brief ({len(confusion_risks)} items) informed diff decisions."
        if confusion_risks
        else "No confusion risks provided in loop brief; template defaults used."
    )
    gate_note = (
        f"Gate threshold met: {valid_count}/{len(misconceptions)} entries have all required fields."
        if gate_passed
        else f"Gate threshold NOT met: only {valid_count}/{len(misconceptions)} entries complete. "
             "Run with a real model_callable to fill stub entries."
    )

    # --- Prepare library write-back (if eligible) ---
    writeback = prepare_library_writeback(
        misconceptions=misconceptions,
        library_entry=library_entry,
        llm_revised_categories=llm_revised_categories,
        quality_warnings=quality_warnings,
        job_id=context.get("job_id", "unknown"),
        family_name=family_name,
        repo_root=repo_root,
    )

    result = {
        "artifact_name": "misconception_map",
        "version": 1,
        "produced_by": "Misconception Architect",
        "timestamp": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "status": status,
        "game_family": family_name,
        "interaction_type": interaction_type,
        "source_confusion_risks": confusion_risks,
        "library_reference_used": library_used,
        "gate_threshold_met": gate_passed,
        "valid_misconception_count": valid_count,
        "misconceptions": misconceptions,
        "notes": f"{source_note} {confusion_note} {gate_note}",
    }

    # Attach write-back as internal key — run() will extract and strip it
    if writeback:
        result["_library_writeback"] = writeback

    return result


# ---------------------------------------------------------------------------
# Library write-back
# ---------------------------------------------------------------------------

def _compute_field_diff(
    original: Dict[str, Any],
    revised: Dict[str, Any],
) -> Dict[str, Dict[str, str]]:
    """Compute a field-level diff between original and revised entries.

    Returns a dict of changed fields, each with "old" and "new" values.
    Only includes fields that actually differ.
    """
    diff: Dict[str, Dict[str, str]] = {}
    for field in _REQUIRED_FIELDS:
        old_val = original.get(field, "")
        new_val = revised.get(field, "")
        if old_val != new_val:
            diff[field] = {"old": str(old_val), "new": str(new_val)}
    return diff


def prepare_library_writeback(
    misconceptions: List[Dict[str, Any]],
    library_entry: Optional[Dict],
    llm_revised_categories: List[str],
    quality_warnings: List[str],
    job_id: str,
    family_name: str,
    repo_root: Path,
) -> Optional[Dict[str, Any]]:
    """Prepare a pending library write-back for revised primary entries.

    Returns a write-back descriptor dict if there are eligible entries,
    or None if nothing qualifies. Does NOT write any files.

    Eligibility:
      - entry must be primary (not secondary)
      - entry must have been revised by LLM
      - entry must have passed quality checks (no quality_notes indicating failure)
    """
    if not library_entry or not llm_revised_categories:
        return None

    # Build lookup of originals from library
    lib_by_cat: Dict[str, Dict[str, Any]] = {}
    for m in library_entry.get("misconceptions", []):
        cat = m.get("category")
        if cat:
            lib_by_cat[cat] = m

    candidates: List[Dict[str, Any]] = []
    for m in misconceptions:
        cat = m.get("category", "")
        if cat not in llm_revised_categories:
            continue
        if m.get("priority") != "primary":
            continue
        # Skip entries that failed quality checks
        qn = m.get("quality_notes", "")
        if "Failed" in qn or "failed" in qn:
            continue

        original = lib_by_cat.get(cat)
        if not original:
            continue

        field_diff = _compute_field_diff(original, m)
        if not field_diff:
            continue  # No actual changes

        candidates.append({
            "category": cat,
            "entry_id": m.get("id", "unknown"),
            "change_rationale": m.get("change_rationale", ""),
            "fields_changed": list(field_diff.keys()),
            "field_diff": field_diff,
            "revised_entry": {
                k: v for k, v in m.items()
                if k in _REQUIRED_FIELDS  # only the 10 core fields
            },
        })

    if not candidates:
        return None

    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    return {
        "writeback_type": "library_revision",
        "status": "pending_review",
        "game_name": library_entry.get("game_name", family_name),
        "game_family": library_entry.get("game_family", "unknown"),
        "source_job_id": job_id,
        "timestamp": timestamp,
        "library_file": (
            family_name.lower().replace(" ", "-").replace("_", "-")
            + "-misconceptions.json"
        ),
        "entries_to_update": candidates,
        "review_notes": (
            f"Generated by Misconception Architect for job '{job_id}'. "
            f"{len(candidates)} primary entries revised and passed quality checks. "
            "Review the field_diff for each entry before applying."
        ),
    }


def write_pending_writeback(
    writeback: Dict[str, Any],
    repo_root: Path,
) -> Path:
    """Write a pending write-back descriptor to the library's pending/ directory.

    Returns the path to the written file.
    """
    pending_dir = repo_root / "artifacts" / "misconception_library" / "pending"
    pending_dir.mkdir(parents=True, exist_ok=True)

    job_id = writeback["source_job_id"]
    timestamp = writeback["timestamp"].replace(":", "").replace("-", "")
    filename = f"{job_id}_{timestamp}.json"
    path = pending_dir / filename

    with open(path, "w") as f:
        json.dump(writeback, f, indent=2, ensure_ascii=False)

    return path


def apply_library_writeback(
    writeback_path: Path,
    repo_root: Path,
    dry_run: bool = True,
    only_categories: Optional[List[str]] = None,
) -> Dict[str, Any]:
    """Apply a pending write-back to the library.

    Args:
        writeback_path: Path to the pending write-back JSON file.
        repo_root: Repository root.
        dry_run: If True, report what would change without modifying files.
        only_categories: If set, apply only entries whose category is in this list.
                         Entries not in the list are left in pending status.

    Returns a dict with:
      - "applied": bool (False if dry_run)
      - "library_file": path to the library file
      - "entries_updated": list of category names updated
      - "entries_skipped": list of category names skipped (partial apply)
      - "backup_path": path to the backup file (only if applied)
    """
    with open(writeback_path) as f:
        writeback = json.load(f)

    if writeback.get("status") not in ("pending_review", "partially_applied"):
        return {"applied": False, "error": f"Status is '{writeback.get('status')}', expected 'pending_review' or 'partially_applied'"}

    library_file = repo_root / "artifacts" / "misconception_library" / writeback["library_file"]
    if not library_file.exists():
        return {"applied": False, "error": f"Library file not found: {library_file}"}

    with open(library_file) as f:
        library = json.load(f)

    entries_updated = []
    entries_skipped = []
    for candidate in writeback["entries_to_update"]:
        cat = candidate["category"]

        # Skip already-applied entries in a partially_applied file
        if candidate.get("applied"):
            continue

        # Filter by only_categories if specified
        if only_categories and cat not in only_categories:
            entries_skipped.append(cat)
            continue

        revised = candidate["revised_entry"]

        for i, m in enumerate(library["misconceptions"]):
            if m.get("category") == cat:
                if not dry_run:
                    library["misconceptions"][i] = revised
                    candidate["applied"] = True
                entries_updated.append(cat)
                break

    result: Dict[str, Any] = {
        "applied": not dry_run,
        "library_file": str(library_file),
        "entries_updated": entries_updated,
        "entries_skipped": entries_skipped,
    }

    if not dry_run and entries_updated:
        # Write backup
        backup_dir = repo_root / "artifacts" / "misconception_library" / "backups"
        backup_dir.mkdir(parents=True, exist_ok=True)
        timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S")
        backup_path = backup_dir / f"{writeback['library_file']}.{timestamp}.bak"
        with open(library_file) as f:
            original_text = f.read()
        with open(backup_path, "w") as f:
            f.write(original_text)
        result["backup_path"] = str(backup_path)

        # Write updated library
        with open(library_file, "w") as f:
            json.dump(library, f, indent=2, ensure_ascii=False)
            f.write("\n")

        # Update writeback status
        all_applied = all(
            e.get("applied", False) for e in writeback["entries_to_update"]
        )
        if all_applied:
            writeback["status"] = "applied"
        else:
            writeback["status"] = "partially_applied"
        writeback["last_applied_at"] = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        writeback["last_applied_categories"] = entries_updated
        with open(writeback_path, "w") as f:
            json.dump(writeback, f, indent=2, ensure_ascii=False)

    return result


# ---------------------------------------------------------------------------
# Pipeline wiring
# ---------------------------------------------------------------------------

def build_spec(repo_root: Path) -> AgentSpec:
    return AgentSpec(
        agent_name="misconception_architect",
        expected_output_artifact="misconception_map",
        expected_produced_by="Misconception Architect",
        prompt_path=repo_root / "agents" / "misconception_architect" / "prompt.md",
        config_path=repo_root / "agents" / "misconception_architect" / "config.yaml",
        allowed_reads=["lowest_viable_loop_brief", "family_architecture_brief", "interaction_decision_memo"],
        allowed_writes=["misconception_map"],
        max_revision_count=2,
    )


def run(
    repo_root: Path,
    job_id: str,
    artifact_paths: Dict[str, Path],
    model_callable=None,
    targeted_llm: Optional[Callable[[str], str]] = None,
    gate_llm: Optional[Callable[[str], str]] = None,
    enable_writeback: bool = False,
):
    """Run the Misconception Architect.

    Args:
        model_callable: Optional override. If provided, replaces the stub entirely.
        targeted_llm:   Strong model for revised entry rewrites and unmatched risks.
        gate_llm:       Cheap model for semantic routing and keep-vs-revise decisions.
        enable_writeback: If True, write pending library write-back files for
                          revised primary entries that pass quality checks.
    """
    # Capture the write-back descriptor if the stub produces one
    _writeback_holder: Dict[str, Any] = {}

    if model_callable is not None:
        effective_callable = model_callable
    else:
        def _stub_wrapper(context: Dict[str, Any]) -> Dict[str, Any]:
            context["repo_root"] = str(repo_root)
            result = misconception_architect_stub(
                context, targeted_llm=targeted_llm, gate_llm=gate_llm,
            )
            # Extract write-back before SharedAgentRunner validates
            wb = result.pop("_library_writeback", None)
            if wb:
                _writeback_holder["data"] = wb
            return result
        effective_callable = _stub_wrapper

    runner = SharedAgentRunner(repo_root)
    agent_result = runner.run(
        spec=build_spec(repo_root),
        job_id=job_id,
        artifact_paths=artifact_paths,
        model_callable=effective_callable,
    )

    # Handle library write-back after successful validation
    if enable_writeback and "data" in _writeback_holder:
        wb = _writeback_holder["data"]
        pending_path = write_pending_writeback(wb, repo_root)
        agent_result.artifact["_writeback_pending_path"] = str(pending_path)

    return agent_result
