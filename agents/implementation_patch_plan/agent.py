"""
Stage 10 — Implementation Patch Plan Agent

Reads: implementation_plan, prototype_ui_spec, prototype_build_spec
Writes: implementation_patch_plan

Bridges the gap between the architectural blueprint (what to build) and
runnable code (how to build it). Produces a totally ordered patch sequence
with a naming registry, animation contracts, and browser-verifiable acceptance
signals. No code appears in this artifact — only precise build instructions.
"""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict

from utils.shared_agent_runner import AgentSpec, SharedAgentRunner

# ---------------------------------------------------------------------------
# Bakery concept override — Pass 3: feel and UI layer
# ---------------------------------------------------------------------------

_BAKERY_PATCH_PLAN: Dict[str, Any] = {
    "patch_objective": (
        "Add the customer character with bounce reaction, full-screen feedback overlay "
        "with scale-in animation, flying pastry arc animation using getBoundingClientRect "
        "and CSS custom properties, and strengthened reward rhythm to the Bakery prototype."
    ),
    "source_pass": {
        "pass_number": 3,
        "pass_label": "Feel and UI Layer",
        "features_added": [
            "Customer character (👩‍🍳 neutral, 😊 on success) with bounce animation on success",
            "Full-screen feedback overlay (position: fixed, green/red, scale-in entry animation)",
            "Flying pastry arc animation using --dx/--dy CSS custom properties and getBoundingClientRect",
            "Stronger reward rhythm: larger success emoji, text-shadow on feedback text, delayed round advance",
        ],
    },
    "target_files": [
        {
            "file_path": "preview/src/BakeryGame.jsx",
            "operation": "edit",
            "current_state": "Monolithic component — no customer character, basic feedback, no flying animation",
            "post_patch_state": "CustomerTicket with character, FeedbackOverlay full-screen, FlyingPastry wired via trayRef/boxRef",
        },
        {
            "file_path": "preview/src/BakeryGame.css",
            "operation": "edit",
            "current_state": "No customer-character styles, no full-screen overlay, no flying pastry keyframe",
            "post_patch_state": "All Pass 3 visual classes and keyframes added",
        },
    ],
    "patch_sequence": [
        {
            "patch_id": "P3-01",
            "file_path": "preview/src/BakeryGame.jsx",
            "patch_type": "add_constant",
            "change_description": (
                "Add FLY_MS = 380 for flying pastry animation duration. "
                "Confirm SUCCESS_MS = 1500 and OVERSHOOT_MS = 700 are present as named constants."
            ),
            "location_hint": "Top of file, after TARGET_SEQUENCE constant",
            "named_elements": ["constant:FLY_MS", "constant:SUCCESS_MS", "constant:OVERSHOOT_MS"],
            "depends_on": [],
            "rationale": "Animation durations must come from constants so they can be adjusted in one place and referenced in setTimeout calls.",
        },
        {
            "patch_id": "P3-02",
            "file_path": "preview/src/BakeryGame.css",
            "patch_type": "add_css_custom_property",
            "change_description": (
                "Declare --dx and --dy as CSS custom properties inside the .flying-pastry rule. "
                "No default value needed — they are always set inline by the component before the animation runs."
            ),
            "location_hint": "Inside .flying-pastry rule block, before the animation declaration",
            "named_elements": ["css_custom_property:--dx", "css_custom_property:--dy"],
            "depends_on": [],
            "rationale": "The flying arc keyframe reads --dx and --dy to compute the translation vector. Declaring them in the rule makes the dependency explicit.",
        },
        {
            "patch_id": "P3-03",
            "file_path": "preview/src/BakeryGame.css",
            "patch_type": "add_keyframe",
            "change_description": (
                "Add fly-to-box keyframe. "
                "0%: translate(-50%, -50%) scale(1), opacity 1. "
                "50%: translate(calc(-50% + var(--dx)*0.5 - 30px), calc(-50% + var(--dy)*0.5 - 60px)) scale(1.15), opacity 1 — arc peak shifted left and above midpoint for a natural lob. "
                "100%: translate(calc(-50% + var(--dx)), calc(-50% + var(--dy))) scale(0.6), opacity 0."
            ),
            "location_hint": "After .flying-pastry rule block",
            "named_elements": ["keyframe:fly-to-box"],
            "depends_on": ["P3-02"],
            "rationale": "The arc is defined entirely in CSS using the custom properties set by the component at mount time.",
        },
        {
            "patch_id": "P3-04",
            "file_path": "preview/src/BakeryGame.css",
            "patch_type": "add_css_class",
            "change_description": (
                "Add .flying-pastry rule: position fixed, font-size 1.8rem, pointer-events none, "
                "z-index 200, transform translate(-50%,-50%) at rest, animation fly-to-box linear forwards "
                "with duration from inline animationDuration style, will-change transform opacity."
            ),
            "location_hint": "Before fly-to-box keyframe block",
            "named_elements": ["css_class:flying-pastry"],
            "depends_on": ["P3-03"],
            "rationale": "position fixed places the element in viewport coordinates matching getBoundingClientRect output. pointer-events none ensures the element never intercepts tray taps.",
        },
        {
            "patch_id": "P3-05",
            "file_path": "preview/src/BakeryGame.jsx",
            "patch_type": "add_ref",
            "change_description": (
                "Add trayRef = useRef(null) and boxRef = useRef(null) inside BakeryGame. "
                "trayRef attaches to the game-footer div (wrapping PastryTray). "
                "boxRef attaches to the div wrapping PastryBox."
            ),
            "location_hint": "Inside BakeryGame function body, after state declarations",
            "named_elements": ["ref:trayRef", "ref:boxRef"],
            "depends_on": [],
            "rationale": "FlyingPastry needs the bounding rectangles of tray and box to compute --dx and --dy at mount time.",
        },
        {
            "patch_id": "P3-06",
            "file_path": "preview/src/BakeryGame.jsx",
            "patch_type": "add_state_variable",
            "change_description": (
                "Add flyingItems = useState([]) as array of {id: number} objects. "
                "Add nextFlyId = useRef(0) as a monotonic counter for stable React keys."
            ),
            "location_hint": "Inside BakeryGame, after trayRef/boxRef (P3-05)",
            "named_elements": ["state_variable:flyingItems", "ref:nextFlyId"],
            "depends_on": ["P3-05"],
            "rationale": "flyingItems drives the conditional render of FlyingPastry elements. nextFlyId prevents React key collisions across rapid taps.",
        },
        {
            "patch_id": "P3-07",
            "file_path": "preview/src/BakeryGame.jsx",
            "patch_type": "add_component",
            "change_description": (
                "Add FlyingPastry component. Props: id, trayRef, boxRef, onDone. "
                "On mount reads getBoundingClientRect from both refs, computes dx = box center x - tray center x, "
                "dy = box center y - tray center y, sets --dx and --dy as inline CSS custom properties, "
                "sets left and top to tray center coordinates, sets animationDuration to FLY_MS ms. "
                "Calls onDone on onAnimationEnd."
            ),
            "location_hint": "Before BakeryGame root function definition",
            "named_elements": ["component:FlyingPastry", "prop:id", "prop:trayRef", "prop:boxRef", "prop:onDone"],
            "depends_on": ["P3-04", "P3-06"],
            "rationale": "FlyingPastry is a single-use ephemeral component that mounts for one animation cycle then its parent removes it.",
        },
        {
            "patch_id": "P3-08",
            "file_path": "preview/src/BakeryGame.jsx",
            "patch_type": "add_component",
            "change_description": (
                "Add CustomerTicket component. Props: target, roundIndex, totalRounds, roundState. "
                "Outer wrapper: class ticket-row. "
                "Customer character block: class customer-character, adds customer-happy when roundState === SUCCESS. "
                "Emoji element: class customer-emoji, content 👩‍🍳 neutral or 😊 on success. "
                "Label span: class customer-label, text 'Customer'. "
                "Ticket card: class customer-ticket with ticket-label 'Order', ticket-number showing target, ticket-sub showing round progress."
            ),
            "location_hint": "Before FlyingPastry definition",
            "named_elements": [
                "component:CustomerTicket",
                "prop:target", "prop:roundIndex", "prop:totalRounds", "prop:roundState",
                "css_class:ticket-row", "css_class:customer-character", "css_class:customer-happy",
                "css_class:customer-emoji", "css_class:customer-label",
                "css_class:customer-ticket", "css_class:ticket-label", "css_class:ticket-number", "css_class:ticket-sub",
            ],
            "depends_on": [],
            "rationale": "The customer character is the primary emotional anchor for the success state.",
        },
        {
            "patch_id": "P3-09",
            "file_path": "preview/src/BakeryGame.css",
            "patch_type": "add_css_class",
            "change_description": (
                "Add all customer character CSS rules: "
                ".ticket-row (flex row, align-items center, gap 16px), "
                ".customer-character (flex column, align-items center, gap 4px, transition transform 0.2s), "
                ".customer-character.customer-happy (animation character-bounce 0.4s cubic-bezier(0.17,0.89,0.32,1.28)), "
                ".customer-emoji (font-size 3rem, line-height 1, display block), "
                ".customer-label (font-size 0.65rem, uppercase, letter-spacing 0.06em). "
                "Add customer ticket rules: .customer-ticket (white bg, 3px solid border, border-radius, padding, min-width 140px), "
                ".ticket-label (0.75rem uppercase), .ticket-number (3.5rem font-weight 900), .ticket-sub (0.75rem color #999)."
            ),
            "location_hint": "After .game-footer rule, before .pastry-box section",
            "named_elements": [
                "css_class:ticket-row", "css_class:customer-character", "css_class:customer-happy",
                "css_class:customer-emoji", "css_class:customer-label",
                "css_class:customer-ticket", "css_class:ticket-label", "css_class:ticket-number", "css_class:ticket-sub",
            ],
            "depends_on": ["P3-08"],
            "rationale": "CSS must exist before the component that uses it is rendered.",
        },
        {
            "patch_id": "P3-10",
            "file_path": "preview/src/BakeryGame.css",
            "patch_type": "add_keyframe",
            "change_description": (
                "Add character-bounce keyframe: "
                "0% scale(1), 50% scale(1.25) translateY(-6px), 100% scale(1). "
                "Applied to .customer-character.customer-happy at 0.4s with cubic-bezier(0.17,0.89,0.32,1.28)."
            ),
            "location_hint": "After .customer-character.customer-happy rule",
            "named_elements": ["keyframe:character-bounce"],
            "depends_on": ["P3-09"],
            "rationale": "The overshoot cubic-bezier produces a physical bounce feeling, not just a scale switch.",
        },
        {
            "patch_id": "P3-11",
            "file_path": "preview/src/BakeryGame.jsx",
            "patch_type": "add_component",
            "change_description": (
                "Add FeedbackOverlay component. Props: roundState. "
                "Returns null when roundState is neither SUCCESS nor OVERSHOOT. "
                "When visible: div class feedback-fullscreen plus feedback-success (success) or feedback-overshoot (overshoot). "
                "Inside: feedback-inner div containing feedback-emoji (😊/↩️) and feedback-text ('Perfect order!' / 'Too many! One bounced back.')."
            ),
            "location_hint": "Before CustomerTicket definition",
            "named_elements": [
                "component:FeedbackOverlay",
                "css_class:feedback-fullscreen", "css_class:feedback-success", "css_class:feedback-overshoot",
                "css_class:feedback-inner", "css_class:feedback-emoji", "css_class:feedback-text",
            ],
            "depends_on": [],
            "rationale": "FeedbackOverlay is independent of CustomerTicket and FlyingPastry and can be defined first.",
        },
        {
            "patch_id": "P3-12",
            "file_path": "preview/src/BakeryGame.css",
            "patch_type": "add_css_class",
            "change_description": (
                "Add full-screen overlay rules. "
                ".feedback-fullscreen: position fixed, inset 0, z-index 100, flex center, pointer-events none, "
                "animation overlay-scale-in 0.18s cubic-bezier(0.17,0.89,0.32,1.2) forwards. "
                ".feedback-fullscreen.feedback-success: background rgba(40,120,60,0.92). "
                ".feedback-fullscreen.feedback-overshoot: background rgba(180,40,30,0.88). "
                ".feedback-inner: text-align center, color #fff. "
                ".feedback-emoji: font-size 5rem, display block, animation emoji-pop 0.25s cubic-bezier(0.17,0.89,0.32,1.4) 0.1s both. "
                ".feedback-text: font-size 1.6rem, font-weight 800, margin-top 16px, text-shadow 0 2px 8px rgba(0,0,0,0.25)."
            ),
            "location_hint": "After .game-shake keyframe block",
            "named_elements": [
                "css_class:feedback-fullscreen", "css_class:feedback-success", "css_class:feedback-overshoot",
                "css_class:feedback-inner", "css_class:feedback-emoji", "css_class:feedback-text",
            ],
            "depends_on": ["P3-11"],
            "rationale": "z-index 100 exceeds game-header z-index 1, ensuring the overlay covers the entire game chrome. pointer-events none keeps isAnimating as the authoritative input gate.",
        },
        {
            "patch_id": "P3-13",
            "file_path": "preview/src/BakeryGame.css",
            "patch_type": "add_keyframe",
            "change_description": (
                "Add overlay-scale-in keyframe: from opacity 0 scale(0.88) to opacity 1 scale(1). "
                "Add emoji-pop keyframe: from scale(0.4) opacity 0 to scale(1) opacity 1."
            ),
            "location_hint": "After .feedback-text rule",
            "named_elements": ["keyframe:overlay-scale-in", "keyframe:emoji-pop"],
            "depends_on": ["P3-12"],
            "rationale": "overlay-scale-in makes the overlay feel like it lands. emoji-pop is delayed 0.1s so it appears after the background, establishing visual hierarchy in time.",
        },
        {
            "patch_id": "P3-14",
            "file_path": "preview/src/BakeryGame.jsx",
            "patch_type": "edit_event_handler",
            "change_description": (
                "Update handleTap to: (1) set isAnimating true at start, "
                "(2) append {id: nextFlyId.current++} to flyingItems to launch a flying item, "
                "(3) wrap total evaluation in setTimeout of FLY_MS so box total updates only after arc completes, "
                "(4) restore isAnimating false after the full feedback cycle (SUCCESS_MS or OVERSHOOT_MS) completes."
            ),
            "location_hint": "Inside BakeryGame, handleTap callback",
            "named_elements": [
                "state_variable:flyingItems", "ref:nextFlyId",
                "callback:handleTap", "constant:FLY_MS", "constant:SUCCESS_MS", "constant:OVERSHOOT_MS",
            ],
            "depends_on": ["P3-06", "P3-01"],
            "rationale": "The FLY_MS delay before total updates is the key timing coordination — the count must not change until the pastry visibly lands.",
        },
        {
            "patch_id": "P3-15",
            "file_path": "preview/src/BakeryGame.jsx",
            "patch_type": "wire_callback",
            "change_description": (
                "Add removeFlyingItem as useCallback that filters flyingItems by id. "
                "Wire it as the onDone prop passed to each FlyingPastry in the render output."
            ),
            "location_hint": "Inside BakeryGame, after handleTap definition",
            "named_elements": ["callback:removeFlyingItem"],
            "depends_on": ["P3-14"],
            "rationale": "FlyingPastry elements must be removed after animation completes to prevent DOM accumulation across rapid taps.",
        },
        {
            "patch_id": "P3-16",
            "file_path": "preview/src/BakeryGame.jsx",
            "patch_type": "edit_render_output",
            "change_description": (
                "Update BakeryGame render: "
                "(1) Add <FeedbackOverlay roundState={roundState} /> as first child of root div, before header. "
                "(2) Map flyingItems to <FlyingPastry key={f.id} id={f.id} trayRef={trayRef} boxRef={boxRef} onDone={() => removeFlyingItem(f.id)} /> as direct root div children. "
                "(3) Replace customer ticket markup in play area with <CustomerTicket target={target} roundIndex={roundIndex} totalRounds={totalRounds} roundState={roundState} />. "
                "(4) Attach ref={boxRef} to wrapper div around PastryBox. "
                "(5) Attach ref={trayRef} to game-footer div."
            ),
            "location_hint": "BakeryGame return statement",
            "named_elements": ["ref:trayRef", "ref:boxRef"],
            "depends_on": ["P3-07", "P3-08", "P3-11", "P3-15"],
            "rationale": "Final wiring patch. Connects all new components and refs into the render tree. Must run last.",
        },
    ],
    "naming_registry": [
        {"name": "FLY_MS",            "name_type": "constant",           "file_path": "preview/src/BakeryGame.jsx", "purpose": "Flying pastry animation duration in ms"},
        {"name": "SUCCESS_MS",         "name_type": "constant",           "file_path": "preview/src/BakeryGame.jsx", "purpose": "Success feedback display duration in ms"},
        {"name": "OVERSHOOT_MS",       "name_type": "constant",           "file_path": "preview/src/BakeryGame.jsx", "purpose": "Overshoot feedback and bounce-back duration in ms"},
        {"name": "--dx",               "name_type": "css_custom_property","file_path": "preview/src/BakeryGame.css", "purpose": "Horizontal translation delta for fly-to-box keyframe"},
        {"name": "--dy",               "name_type": "css_custom_property","file_path": "preview/src/BakeryGame.css", "purpose": "Vertical translation delta for fly-to-box keyframe"},
        {"name": "fly-to-box",         "name_type": "keyframe",           "file_path": "preview/src/BakeryGame.css", "purpose": "Arc animation from tray center to box center"},
        {"name": "flying-pastry",      "name_type": "css_class",          "file_path": "preview/src/BakeryGame.css", "purpose": "Fixed-position animated emoji element"},
        {"name": "character-bounce",   "name_type": "keyframe",           "file_path": "preview/src/BakeryGame.css", "purpose": "Bounce animation triggered by customer-happy class"},
        {"name": "ticket-row",         "name_type": "css_class",          "file_path": "preview/src/BakeryGame.css", "purpose": "Flex row containing character and ticket card"},
        {"name": "customer-character", "name_type": "css_class",          "file_path": "preview/src/BakeryGame.css", "purpose": "Customer emoji column wrapper"},
        {"name": "customer-happy",     "name_type": "css_class",          "file_path": "preview/src/BakeryGame.css", "purpose": "Applied on SUCCESS state to trigger bounce animation"},
        {"name": "customer-emoji",     "name_type": "css_class",          "file_path": "preview/src/BakeryGame.css", "purpose": "The emoji element inside character wrapper"},
        {"name": "customer-label",     "name_type": "css_class",          "file_path": "preview/src/BakeryGame.css", "purpose": "'Customer' label below the emoji"},
        {"name": "customer-ticket",    "name_type": "css_class",          "file_path": "preview/src/BakeryGame.css", "purpose": "The ticket card box"},
        {"name": "ticket-label",       "name_type": "css_class",          "file_path": "preview/src/BakeryGame.css", "purpose": "'Order' label above target number"},
        {"name": "ticket-number",      "name_type": "css_class",          "file_path": "preview/src/BakeryGame.css", "purpose": "Large target number display"},
        {"name": "ticket-sub",         "name_type": "css_class",          "file_path": "preview/src/BakeryGame.css", "purpose": "Round progress indicator"},
        {"name": "overlay-scale-in",   "name_type": "keyframe",           "file_path": "preview/src/BakeryGame.css", "purpose": "Scale-in entry animation for feedback overlay"},
        {"name": "emoji-pop",          "name_type": "keyframe",           "file_path": "preview/src/BakeryGame.css", "purpose": "Delayed pop-in for the feedback emoji"},
        {"name": "feedback-fullscreen","name_type": "css_class",          "file_path": "preview/src/BakeryGame.css", "purpose": "Fixed, inset-0 overlay container"},
        {"name": "feedback-success",   "name_type": "css_class",          "file_path": "preview/src/BakeryGame.css", "purpose": "Green background variant for success state"},
        {"name": "feedback-overshoot", "name_type": "css_class",          "file_path": "preview/src/BakeryGame.css", "purpose": "Red background variant for overshoot state"},
        {"name": "feedback-inner",     "name_type": "css_class",          "file_path": "preview/src/BakeryGame.css", "purpose": "Centered content wrapper inside overlay"},
        {"name": "feedback-emoji",     "name_type": "css_class",          "file_path": "preview/src/BakeryGame.css", "purpose": "Large emoji inside overlay"},
        {"name": "feedback-text",      "name_type": "css_class",          "file_path": "preview/src/BakeryGame.css", "purpose": "Message text with text-shadow"},
        {"name": "trayRef",            "name_type": "ref",                "file_path": "preview/src/BakeryGame.jsx", "purpose": "DOM ref for PastryTray footer wrapper"},
        {"name": "boxRef",             "name_type": "ref",                "file_path": "preview/src/BakeryGame.jsx", "purpose": "DOM ref for PastryBox wrapper"},
        {"name": "flyingItems",        "name_type": "state_variable",     "file_path": "preview/src/BakeryGame.jsx", "purpose": "Array of active flying pastry instances"},
        {"name": "nextFlyId",          "name_type": "ref",                "file_path": "preview/src/BakeryGame.jsx", "purpose": "Monotonic counter for stable React keys"},
        {"name": "removeFlyingItem",   "name_type": "callback",           "file_path": "preview/src/BakeryGame.jsx", "purpose": "Removes a completed FlyingPastry by id"},
        {"name": "FlyingPastry",       "name_type": "component",          "file_path": "preview/src/BakeryGame.jsx", "purpose": "Single-use arc animation component"},
        {"name": "CustomerTicket",     "name_type": "component",          "file_path": "preview/src/BakeryGame.jsx", "purpose": "Customer character plus order ticket card"},
        {"name": "FeedbackOverlay",    "name_type": "component",          "file_path": "preview/src/BakeryGame.jsx", "purpose": "Full-screen success/overshoot overlay"},
        {"name": "id",                 "name_type": "prop",               "file_path": "preview/src/BakeryGame.jsx", "purpose": "Unique key for each FlyingPastry instance"},
        {"name": "onDone",             "name_type": "prop",               "file_path": "preview/src/BakeryGame.jsx", "purpose": "Callback fired by FlyingPastry when animation completes"},
        {"name": "target",             "name_type": "prop",               "file_path": "preview/src/BakeryGame.jsx", "purpose": "Current round target number passed to CustomerTicket"},
        {"name": "roundIndex",         "name_type": "prop",               "file_path": "preview/src/BakeryGame.jsx", "purpose": "0-based current round index passed to CustomerTicket"},
        {"name": "totalRounds",        "name_type": "prop",               "file_path": "preview/src/BakeryGame.jsx", "purpose": "Total number of rounds in the session"},
        {"name": "roundState",         "name_type": "prop",               "file_path": "preview/src/BakeryGame.jsx", "purpose": "Current round state string driving CustomerTicket expression and overlay variant"},
        {"name": "handleTap",          "name_type": "callback",           "file_path": "preview/src/BakeryGame.jsx", "purpose": "Tap handler passed to PastryTray; fires flying pastry and increments total"},
    ],
    "animation_contracts": [
        {
            "animation_id": "fly-to-box",
            "trigger": "FlyingPastry mounts (one instance per tap)",
            "duration_ms": 380,
            "easing": "linear",
            "css_custom_properties": ["--dx", "--dy"],
            "keyframe_name": "fly-to-box",
            "owner_file": "preview/src/BakeryGame.css",
            "element_selector": ".flying-pastry",
            "dom_measurement_required": True,
        },
        {
            "animation_id": "character-bounce",
            "trigger": "customer-happy class applied when roundState === SUCCESS",
            "duration_ms": 400,
            "easing": "cubic-bezier(0.17, 0.89, 0.32, 1.28)",
            "css_custom_properties": [],
            "keyframe_name": "character-bounce",
            "owner_file": "preview/src/BakeryGame.css",
            "element_selector": ".customer-character.customer-happy",
            "dom_measurement_required": False,
        },
        {
            "animation_id": "overlay-scale-in",
            "trigger": ".feedback-fullscreen element mounts",
            "duration_ms": 180,
            "easing": "cubic-bezier(0.17, 0.89, 0.32, 1.2)",
            "css_custom_properties": [],
            "keyframe_name": "overlay-scale-in",
            "owner_file": "preview/src/BakeryGame.css",
            "element_selector": ".feedback-fullscreen",
            "dom_measurement_required": False,
        },
        {
            "animation_id": "emoji-pop",
            "trigger": ".feedback-emoji mounts with 0.1s delay after overlay",
            "duration_ms": 250,
            "easing": "cubic-bezier(0.17, 0.89, 0.32, 1.4)",
            "css_custom_properties": [],
            "keyframe_name": "emoji-pop",
            "owner_file": "preview/src/BakeryGame.css",
            "element_selector": ".feedback-emoji",
            "dom_measurement_required": False,
        },
    ],
    "acceptance_signals": [
        {"signal_id": "AS3-01", "description": "Customer character visible in neutral state",                  "observable_in_browser": "👩‍🍳 appears left of ticket card on every round start",                                            "related_patches": ["P3-08", "P3-09", "P3-16"]},
        {"signal_id": "AS3-02", "description": "Customer reacts on success with bounce",                       "observable_in_browser": "On exact match character switches to 😊 and visibly bounces upward then returns",              "related_patches": ["P3-08", "P3-09", "P3-10", "P3-16"]},
        {"signal_id": "AS3-03", "description": "Full-screen green overlay on success",                         "observable_in_browser": "Entire screen turns green-tinted overlapping header, play area, and footer",                   "related_patches": ["P3-11", "P3-12", "P3-13", "P3-16"]},
        {"signal_id": "AS3-04", "description": "Full-screen red overlay on overshoot",                         "observable_in_browser": "Entire screen turns red-tinted on overshoot with same full coverage",                          "related_patches": ["P3-11", "P3-12", "P3-13", "P3-16"]},
        {"signal_id": "AS3-05", "description": "Overlay scales in rather than appearing instantly",             "observable_in_browser": "Success and overshoot overlays animate from slightly smaller to full size on entry",             "related_patches": ["P3-12", "P3-13"]},
        {"signal_id": "AS3-06", "description": "Large emoji in overlay pops in with delay",                    "observable_in_browser": "5rem emoji appears with delayed pop-in after overlay background establishes",                   "related_patches": ["P3-12", "P3-13"]},
        {"signal_id": "AS3-07", "description": "Feedback text has visible text-shadow",                        "observable_in_browser": "'Perfect order!' text is legible against colored background with a visible shadow",             "related_patches": ["P3-12"]},
        {"signal_id": "AS3-08", "description": "Pastry visibly travels from tray to box",                      "observable_in_browser": "🥐 emoji travels in an arc from footer tray area upward to pastry box before disappearing",    "related_patches": ["P3-03", "P3-04", "P3-07", "P3-14", "P3-16"]},
        {"signal_id": "AS3-09", "description": "Box total updates only after pastry lands",                    "observable_in_browser": "Running total in header does not increment until flying pastry animation completes",            "related_patches": ["P3-01", "P3-14"]},
        {"signal_id": "AS3-10", "description": "Multiple rapid taps do not cause multiple simultaneous flights","observable_in_browser": "isAnimating blocks subsequent taps during the arc — only one pastry flies per tap cycle",      "related_patches": ["P3-14", "P3-16"]},
    ],
    "patch_notes": (
        "Pass 3 patches apply on top of the Pass 2 codebase. "
        "The FlyingPastry DOM measurement reads getBoundingClientRect at component mount time, not at tap time. "
        "This is correct sequencing: the element mounts, reads the DOM, sets custom properties, then the browser paints the first animation frame. "
        "The --dx/--dy approach keeps all animation curve definitions in CSS. "
        "Z-index stack: game chrome z-index 1, FeedbackOverlay z-index 100, FlyingPastry z-index 200 — "
        "a flying pastry launched just before success lands on top of the green flash, which is the correct visual priority. "
        "The delayed round advance (SUCCESS_MS after success state is set) is unchanged from Pass 2."
    ),
}

# ---------------------------------------------------------------------------
# Generic fallback
# ---------------------------------------------------------------------------

_GENERIC_PATCH_PLAN: Dict[str, Any] = {
    "patch_objective": "Apply Pass 1 core loop changes to the prototype codebase.",
    "source_pass": {
        "pass_number": 1,
        "pass_label": "Core Loop",
        "features_added": ["Core interaction loop", "Target matching mechanic", "Basic feedback states"],
    },
    "target_files": [
        {
            "file_path": "preview/src/Game.jsx",
            "operation": "create",
            "current_state": "File does not exist",
            "post_patch_state": "Root game component with state machine and render output",
        },
        {
            "file_path": "preview/src/Game.css",
            "operation": "create",
            "current_state": "File does not exist",
            "post_patch_state": "All visual styles for core loop",
        },
    ],
    "patch_sequence": [
        {
            "patch_id": "P1-01",
            "file_path": "preview/src/Game.jsx",
            "patch_type": "add_constant",
            "change_description": "Add game constants: target sequence, state enum, timing constants.",
            "location_hint": "Top of file",
            "named_elements": ["constant:TARGET_SEQUENCE", "constant:STATES"],
            "depends_on": [],
            "rationale": "Constants must be defined before any component references them.",
        },
    ],
    "naming_registry": [
        {"name": "TARGET_SEQUENCE", "name_type": "constant", "file_path": "preview/src/Game.jsx", "purpose": "Ordered list of target values for the game session"},
        {"name": "STATES",          "name_type": "constant", "file_path": "preview/src/Game.jsx", "purpose": "Enum of game state machine states"},
    ],
    "animation_contracts": [],
    "acceptance_signals": [
        {
            "signal_id": "AS1-01",
            "description": "Core loop runs — tap adds item, total updates, success state triggers on match",
            "observable_in_browser": "Tapping an item increments the running total; reaching the target shows success feedback",
            "related_patches": ["P1-01"],
        },
    ],
    "patch_notes": "Generic fallback stub — replace with game-specific patch plan for production use.",
}

CONCEPT_OVERRIDES: Dict[str, Dict[str, Any]] = {
    "bakery": _BAKERY_PATCH_PLAN,
}

# ---------------------------------------------------------------------------
# Stub callable
# ---------------------------------------------------------------------------


def implementation_patch_plan_stub(context: Dict[str, Any]) -> Dict[str, Any]:
    # Read world_theme from implementation_plan (available in allowed_reads).
    # Fall back to prototype_spec if present (legacy path).
    artifact_inputs = context.get("artifact_inputs", {})
    impl_plan = artifact_inputs.get("implementation_plan", {})
    world_theme = (
        impl_plan.get("implementation_goal", "")
        + " "
        + " ".join(
            f.get("path", "") for f in impl_plan.get("file_plan", [])
        )
    )
    if not world_theme.strip():
        proto = artifact_inputs.get("prototype_spec", {})
        world_theme = proto.get("concept_anchor", {}).get("world_theme", "")

    concept_key = None
    for key in CONCEPT_OVERRIDES:
        if key in world_theme.lower():
            concept_key = key
            break

    plan = CONCEPT_OVERRIDES[concept_key] if concept_key else _GENERIC_PATCH_PLAN

    return {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "status": "pass",
        "patch_objective":    plan["patch_objective"],
        "source_pass":        plan["source_pass"],
        "target_files":       plan["target_files"],
        "patch_sequence":     plan["patch_sequence"],
        "naming_registry":    plan["naming_registry"],
        "animation_contracts": plan["animation_contracts"],
        "acceptance_signals": plan["acceptance_signals"],
        "patch_notes":        plan["patch_notes"],
    }


# ---------------------------------------------------------------------------
# AgentSpec
# ---------------------------------------------------------------------------


def build_spec(repo_root: Path) -> AgentSpec:
    return AgentSpec(
        agent_name="implementation_patch_plan_agent",
        expected_output_artifact="implementation_patch_plan",
        expected_produced_by="Implementation Patch Plan Agent",
        prompt_path=repo_root / "agents" / "implementation_patch_plan" / "prompt.md",
        config_path=repo_root / "agents" / "implementation_patch_plan" / "config.yaml",
        allowed_reads=["implementation_plan", "prototype_ui_spec", "prototype_build_spec"],
        allowed_writes=["implementation_patch_plan"],
        max_revision_count=2,
    )


# ---------------------------------------------------------------------------
# run()
# ---------------------------------------------------------------------------


def run(repo_root: Path, job_id: str, artifact_paths: Dict[str, Path], model_callable=None):
    runner = SharedAgentRunner(repo_root)
    return runner.run(
        spec=build_spec(repo_root),
        job_id=job_id,
        artifact_paths=artifact_paths,
        model_callable=model_callable if model_callable is not None else implementation_patch_plan_stub,
    )
