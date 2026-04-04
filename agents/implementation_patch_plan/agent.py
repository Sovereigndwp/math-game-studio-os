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
# Bakery concept override — Pass 1: Core Playable Loop
# Creates all files declared in implementation_plan.file_plan
# ---------------------------------------------------------------------------

_BAKERY_PATCH_PLAN: Dict[str, Any] = {
    "patch_objective": (
        "Create the initial playable Bakery Rush prototype: level config data, "
        "all five UI components (OrderTicket, ConveyorBelt, PastryBox, ShiftHUD, FeedbackOverlay), "
        "styles, and the BakeryRushPrototype root container wired with full game state and loop logic."
    ),
    "source_pass": {
        "pass_number": 1,
        "pass_label": "Core Playable Loop",
        "features_added": [
            "Level config data: 5 levels with conveyorSpeed, targetPool, pastryWeights, patience, scoreThreshold",
            "OrderTicket component: displays current customer, target value, and patience bar",
            "ConveyorBelt component: renders moving pastry items with tap-to-select interaction",
            "PastryBox component: renders box contents, running total, and overshoot/success visual response",
            "ShiftHUD component: renders score, lives, patience bar, queue preview, and level indicator",
            "FeedbackOverlay component: renders full-screen success, overshoot, and end-of-shift states",
            "BakeryRushPrototype: root game container with full session state, timers, and loop orchestration",
        ],
    },
    "target_files": [
        {
            "file_path": "preview/src/App.jsx",
            "operation": "edit",
            "current_state": "Mounts previous game component or placeholder",
            "post_patch_state": "Mounts BakeryRushPrototype as the active game component",
        },
        {
            "file_path": "preview/src/games/BakeryRushPrototype.jsx",
            "operation": "create",
            "current_state": "File does not exist",
            "post_patch_state": "Root container with full game state, timers, queue management, and child component wiring",
        },
        {
            "file_path": "preview/src/games/bakery/levelConfig.js",
            "operation": "create",
            "current_state": "File does not exist",
            "post_patch_state": "Exports levelConfigs array and PASTRY_VALUES constant",
        },
        {
            "file_path": "preview/src/games/bakery/components/OrderTicket.jsx",
            "operation": "create",
            "current_state": "File does not exist",
            "post_patch_state": "Presentational component showing customer identity, target value, and patience bar",
        },
        {
            "file_path": "preview/src/games/bakery/components/ConveyorBelt.jsx",
            "operation": "create",
            "current_state": "File does not exist",
            "post_patch_state": "Animated horizontal conveyor with tap-to-select pastry items",
        },
        {
            "file_path": "preview/src/games/bakery/components/PastryBox.jsx",
            "operation": "create",
            "current_state": "File does not exist",
            "post_patch_state": "Box contents grid with running total and feedback (overshoot shake, success glow)",
        },
        {
            "file_path": "preview/src/games/bakery/components/ShiftHUD.jsx",
            "operation": "create",
            "current_state": "File does not exist",
            "post_patch_state": "Persistent HUD strip: score, lives, patience bar, queue preview, level badge",
        },
        {
            "file_path": "preview/src/games/bakery/components/FeedbackOverlay.jsx",
            "operation": "create",
            "current_state": "File does not exist",
            "post_patch_state": "Full-screen overlay for SUCCESS, OVERSHOOT, and END_OF_SHIFT feedback states",
        },
        {
            "file_path": "preview/src/games/bakery/styles.css",
            "operation": "create",
            "current_state": "File does not exist",
            "post_patch_state": "All layout, motion, and readability styles scoped to .bakery-rush class",
        },
    ],
    "patch_sequence": [
        {
            "patch_id": "P1-01",
            "file_path": "preview/src/games/bakery/levelConfig.js",
            "patch_type": "add_constant",
            "change_description": (
                "Export levelConfigs as the default export — an array of 5 objects. "
                "Each object: conveyorSpeed (number, pixels/sec), targetPool (array of integers), "
                "pastryWeights (object mapping emoji to relative frequency weight), "
                "patience (integer seconds), scoreThreshold (integer), streakBonus (integer). "
                "Level 1: speed 80, targets [4,5,6,7,8], patience 20. "
                "Level 2: speed 110, targets [5,6,7,8,10,12], patience 18. "
                "Level 3: speed 140, targets [5,7,9,12,15], patience 15. "
                "Level 4: speed 180, targets [6,8,10,14,18], patience 12. "
                "Level 5: speed 220, targets [8,10,12,16,20], patience 10."
            ),
            "location_hint": "Top of file, default export",
            "named_elements": ["constant:levelConfigs"],
            "depends_on": [],
            "rationale": "Level config must be defined before any component imports it.",
        },
        {
            "patch_id": "P1-02",
            "file_path": "preview/src/games/bakery/levelConfig.js",
            "patch_type": "add_constant",
            "change_description": (
                "Export PASTRY_VALUES as a named const object mapping pastry emoji keys to numeric values. "
                "Entries: '🥐': 1, '🍩': 2, '🧁': 3, '🍰': 4, '🎂': 5. "
                "This is the authoritative source for pastry math values used by BakeryRushPrototype."
            ),
            "location_hint": "After levelConfigs default export",
            "named_elements": ["constant:PASTRY_VALUES"],
            "depends_on": ["P1-01"],
            "rationale": "Centralizing pastry math values prevents magic numbers in component logic.",
        },
        {
            "patch_id": "P1-03",
            "file_path": "preview/src/games/bakery/styles.css",
            "patch_type": "add_css_class",
            "change_description": (
                "Create the full stylesheet. "
                "Root: .bakery-rush (flex column, 100vh, font-family sans-serif, overflow hidden, background #fdf6ec). "
                "Conveyor: .conveyor-belt (overflow hidden, position relative, height 120px). "
                ".belt-track (display flex, gap 16px, animation belt-scroll linear infinite, "
                "animation-duration var(--belt-duration, 4s), will-change transform). "
                "Belt item: .belt-item (flex column, align-items center, cursor pointer, padding 8px, "
                "border-radius 12px, transition background 0.15s). "
                ".belt-item:hover (background rgba(0,0,0,0.06)). "
                ".belt-item-disabled (opacity 0.4, pointer-events none). "
                "Patience bar: .patience-bar (height 6px, background #e5e7eb, border-radius 3px). "
                ".patience-fill (height 100%, background #f59e0b, border-radius 3px, transition width 0.3s linear). "
                "Same for .hud-patience-bar and .hud-patience-fill. "
                "Pastry box: .pastry-box (border 3px solid #d1d5db, border-radius 16px, padding 16px, "
                "transition box-shadow 0.2s). "
                ".box-success (box-shadow 0 0 24px rgba(40,160,80,0.6), border-color #22c55e). "
                ".box-overshoot (animation box-shake 0.35s ease). "
                "Overlay: .feedback-overlay (position fixed, inset 0, z-index 50, display flex, "
                "align-items center, justify-content center, "
                "animation overlay-enter 0.18s cubic-bezier(0.17,0.89,0.32,1.1) forwards). "
                ".overlay-success (background rgba(30,120,50,0.93)). "
                ".overlay-overshoot (background rgba(180,40,30,0.9)). "
                ".overlay-end (background rgba(20,60,140,0.92)). "
                ".overlay-inner (text-align center, color #fff). "
                ".overlay-emoji (font-size 5rem, display block). "
                ".overlay-title (font-size 2rem, font-weight 800, margin-top 12px). "
                ".overlay-subtitle (font-size 1.1rem, margin-top 8px, opacity 0.9). "
                ".overlay-stats (margin-top 16px, font-size 1rem, opacity 0.85). "
                "HUD: .shift-hud (display flex, align-items center, gap 16px, padding 12px 16px, "
                "background #fff, border-bottom 1px solid #e5e7eb). "
                ".hud-level-badge (background #6366f1, color #fff, border-radius 999px, "
                "padding 2px 10px, font-size 0.8rem, font-weight 700). "
                ".hud-queue (display flex, gap 8px). "
                ".hud-queue-item (font-size 0.75rem, background #f3f4f6, border-radius 8px, padding 4px 8px). "
            ),
            "location_hint": "Full file content — new file",
            "named_elements": [
                "css_class:bakery-rush",
                "css_class:conveyor-belt", "css_class:belt-track",
                "css_class:belt-item", "css_class:belt-item-disabled",
                "css_class:pastry-emoji", "css_class:pastry-value",
                "css_class:patience-bar", "css_class:patience-fill",
                "css_class:hud-patience-bar", "css_class:hud-patience-fill",
                "css_class:pastry-box", "css_class:box-success", "css_class:box-overshoot",
                "css_class:box-items-grid", "css_class:box-item",
                "css_class:box-total-row", "css_class:box-total-label", "css_class:box-total-value",
                "css_class:box-target-label",
                "css_class:feedback-overlay", "css_class:overlay-success",
                "css_class:overlay-overshoot", "css_class:overlay-end",
                "css_class:overlay-inner", "css_class:overlay-emoji",
                "css_class:overlay-title", "css_class:overlay-subtitle", "css_class:overlay-stats",
                "css_class:shift-hud", "css_class:hud-score-label", "css_class:hud-score-value",
                "css_class:hud-lives", "css_class:hud-level-badge",
                "css_class:hud-queue", "css_class:hud-queue-item",
                "css_class:order-ticket", "css_class:order-target-label", "css_class:order-target-value",
                "css_class:order-message",
                "css_custom_property:--belt-duration",
                "keyframe:belt-scroll", "keyframe:box-shake", "keyframe:overlay-enter",
            ],
            "depends_on": [],
            "rationale": "All shared keyframes and layout primitives must exist before any component imports the stylesheet.",
        },
        {
            "patch_id": "P1-04",
            "file_path": "preview/src/games/bakery/styles.css",
            "patch_type": "add_keyframe",
            "change_description": (
                "Add three keyframes. "
                "belt-scroll: from translateX(0) to translateX(-50%) — "
                "the track renders items twice so the scroll loops seamlessly. "
                "box-shake: 0% translateX(0), 20% translateX(-8px), 40% translateX(8px), "
                "60% translateX(-6px), 80% translateX(6px), 100% translateX(0) — "
                "a horizontal rejection shake for overshoot. "
                "overlay-enter: from (opacity 0, scale(0.88)) to (opacity 1, scale(1)) — "
                "snappy scale-in entry for the full-screen overlay."
            ),
            "location_hint": "After all CSS class rules, at end of file",
            "named_elements": ["keyframe:belt-scroll", "keyframe:box-shake", "keyframe:overlay-enter"],
            "depends_on": ["P1-03"],
            "rationale": "Keyframes must be defined in the same file as the classes that reference them.",
        },
        {
            "patch_id": "P1-05",
            "file_path": "preview/src/games/bakery/components/OrderTicket.jsx",
            "patch_type": "add_component",
            "change_description": (
                "Create OrderTicket as a default export function. "
                "Props: currentTarget (number), customerName (string), customerEmoji (string), "
                "patiencePercent (number 0–1), message (string|null). "
                "Render: outer div class order-ticket. "
                "Customer row: customerEmoji in a large span, customerName in a smaller span below. "
                "Target block: order-target-label div ('Order'), order-target-value div (currentTarget as bold number). "
                "Patience bar: patience-bar div wrapping patience-fill div with inline width = patiencePercent * 100 + '%'. "
                "Message area: order-message p, rendered only when message is non-null."
            ),
            "location_hint": "Full file content — new file",
            "named_elements": [
                "component:OrderTicket",
                "prop:currentTarget", "prop:customerName", "prop:customerEmoji",
                "prop:patiencePercent", "prop:message",
            ],
            "depends_on": ["P1-03"],
            "rationale": "OrderTicket is purely presentational. All data comes from props; no internal state.",
        },
        {
            "patch_id": "P1-06",
            "file_path": "preview/src/games/bakery/components/ConveyorBelt.jsx",
            "patch_type": "add_component",
            "change_description": (
                "Create ConveyorBelt as a default export function. "
                "Props: items (array of {id, emoji, value}), beltDuration (number, seconds), "
                "interactionEnabled (boolean), onPastrySelect (function(item) => void). "
                "Render: outer div class conveyor-belt. "
                "Inner div class belt-track with inline style --belt-duration set to beltDuration + 's'. "
                "Render items twice (items.concat(items)) so the loop is seamless. "
                "Each item renders as a belt-item div with pastry-emoji span (item.emoji) and pastry-value span ('+' + item.value). "
                "Apply belt-item-disabled class when interactionEnabled is false. "
                "On click: call onPastrySelect(item) only when interactionEnabled is true. "
                "Add role='button' and tabIndex={0} to each belt-item for keyboard accessibility."
            ),
            "location_hint": "Full file content — new file",
            "named_elements": [
                "component:ConveyorBelt",
                "prop:items", "prop:beltDuration", "prop:interactionEnabled", "prop:onPastrySelect",
            ],
            "depends_on": ["P1-03"],
            "rationale": "ConveyorBelt owns only the interaction surface. Game logic is handled by the onPastrySelect callback.",
        },
        {
            "patch_id": "P1-07",
            "file_path": "preview/src/games/bakery/components/PastryBox.jsx",
            "patch_type": "add_component",
            "change_description": (
                "Create PastryBox as a default export function. "
                "Props: boxItems (array of {id, emoji}), currentTotal (number), currentTarget (number), "
                "feedbackMode (string|null). "
                "Render: outer div class pastry-box. "
                "Apply box-success class when feedbackMode === 'success'. "
                "Apply box-overshoot class when feedbackMode === 'overshoot'. "
                "Items area: box-items-grid div mapping boxItems to box-item spans (each showing item.emoji). "
                "Total display: box-total-row div containing box-total-label span ('Total: ') "
                "and box-total-value span (currentTotal). "
                "Target indicator: box-target-label div ('of ' + currentTarget)."
            ),
            "location_hint": "Full file content — new file",
            "named_elements": [
                "component:PastryBox",
                "prop:boxItems", "prop:currentTotal", "prop:feedbackMode",
            ],
            "depends_on": ["P1-03"],
            "rationale": "PastryBox is purely presentational. feedbackMode drives CSS class-based animations defined in styles.css.",
        },
        {
            "patch_id": "P1-08",
            "file_path": "preview/src/games/bakery/components/ShiftHUD.jsx",
            "patch_type": "add_component",
            "change_description": (
                "Create ShiftHUD as a default export function. "
                "Props: score (number), lives (number), patiencePercent (number 0–1), "
                "levelIndex (number), queue (array of {customerEmoji, targetValue} up to 3 items). "
                "Render: outer div class shift-hud. "
                "Score block: hud-score-label span ('Score') and hud-score-value span. "
                "Lives: hud-lives div rendering '❤️'.repeat(lives). "
                "Level badge: hud-level-badge span ('Lv ' + (levelIndex + 1)). "
                "Queue preview: hud-queue div, each item as hud-queue-item span (customerEmoji + ' ' + targetValue). "
                "Patience strip: hud-patience-bar div wrapping hud-patience-fill div "
                "with inline width = patiencePercent * 100 + '%'."
            ),
            "location_hint": "Full file content — new file",
            "named_elements": [
                "component:ShiftHUD",
                "prop:score", "prop:lives", "prop:patiencePercent", "prop:levelIndex", "prop:queue",
            ],
            "depends_on": ["P1-03"],
            "rationale": "ShiftHUD is purely presentational — all situational awareness data flows in as props.",
        },
        {
            "patch_id": "P1-09",
            "file_path": "preview/src/games/bakery/components/FeedbackOverlay.jsx",
            "patch_type": "add_component",
            "change_description": (
                "Create FeedbackOverlay as a default export function. "
                "Props: feedbackMode (string|null: 'success'|'overshoot'|'end_of_shift'|null), "
                "customerReaction (string emoji), summaryStats ({score, ordersCompleted, streakBest}). "
                "Return null when feedbackMode is null. "
                "Render: outer div class feedback-overlay plus one of overlay-success, overlay-overshoot, overlay-end "
                "depending on feedbackMode. "
                "Inner: overlay-inner div containing overlay-emoji (large emoji), overlay-title (state label string), "
                "overlay-subtitle (contextual message string). "
                "When feedbackMode is 'end_of_shift': also render overlay-stats div showing "
                "Score, Orders Completed, and Best Streak from summaryStats."
            ),
            "location_hint": "Full file content — new file",
            "named_elements": [
                "component:FeedbackOverlay",
                "prop:feedbackMode", "prop:customerReaction", "prop:summaryStats",
            ],
            "depends_on": ["P1-03"],
            "rationale": "FeedbackOverlay is a stateless conditional renderer. feedbackMode is the single switch controlling visibility and variant.",
        },
        {
            "patch_id": "P1-10",
            "file_path": "preview/src/games/BakeryRushPrototype.jsx",
            "patch_type": "add_component",
            "change_description": (
                "Create BakeryRushPrototype as a default export function. "
                "Imports: levelConfigs and PASTRY_VALUES from '../games/bakery/levelConfig'. "
                "Imports: OrderTicket, ConveyorBelt, PastryBox, ShiftHUD, FeedbackOverlay from './bakery/components/'. "
                "Imports: '../games/bakery/styles.css'. "
                "State (all via useState): screenState ('PLAYING'), levelIndex (0), score (0), lives (3), "
                "currentTarget (drawn from levelConfigs[0].targetPool at random), currentTotal (0), "
                "feedbackMode (null), patienceLeft (levelConfigs[0].patience), streak (0), "
                "boxItems ([]), conveyorItems (initial generated list), customerQueue (3 random customer objects), "
                "customerIndex (0). "
                "Derived (computed inline): currentLevelConfig = levelConfigs[levelIndex], "
                "patiencePercent = patienceLeft / currentLevelConfig.patience, "
                "nextLevelUnlocked = score >= currentLevelConfig.scoreThreshold. "
                "SUCCESS_MS = 1200, OVERSHOOT_MS = 700 as module-level constants. "
                "Patience timer: useEffect with setInterval that decrements patienceLeft by 1 each second "
                "when screenState is PLAYING and feedbackMode is null. "
                "On patienceLeft reaching 0: decrement lives by 1, advance to next customer, reset box state. "
                "When lives hits 0: set screenState to END_OF_SHIFT. "
                "handlePastrySelect(item): if feedbackMode is not null, return early. "
                "Look up item.value from PASTRY_VALUES. Append item to boxItems. "
                "Compute newTotal = currentTotal + item.value. "
                "If newTotal === currentTarget: award score, increment streak, set feedbackMode 'success'. "
                "After SUCCESS_MS: advance to next customer, reset box and currentTotal to 0, clear feedbackMode. "
                "If newTotal > currentTarget: set feedbackMode 'overshoot'. "
                "After OVERSHOOT_MS: remove last item from boxItems, set currentTotal back to currentTotal (not newTotal), "
                "clear feedbackMode. "
                "Otherwise: set currentTotal to newTotal. "
                "On nextLevelUnlocked: increment levelIndex (capped at 4), reset customer queue. "
                "Render: root div class bakery-rush. "
                "Always: ShiftHUD with score, lives, patiencePercent, levelIndex, queue slice of customerQueue. "
                "Always: FeedbackOverlay with feedbackMode, customerReaction, summaryStats. "
                "When screenState is PLAYING: OrderTicket (currentTarget, current customer emoji/name, patiencePercent, null message), "
                "ConveyorBelt (conveyorItems, beltDuration derived from currentLevelConfig.conveyorSpeed, "
                "interactionEnabled = feedbackMode is null, onPastrySelect = handlePastrySelect), "
                "PastryBox (boxItems, currentTotal, currentTarget, feedbackMode)."
            ),
            "location_hint": "Full file content — new file",
            "named_elements": [
                "component:BakeryRushPrototype",
                "state_variable:screenState", "state_variable:levelIndex", "state_variable:score",
                "state_variable:lives", "state_variable:currentTarget", "state_variable:currentTotal",
                "state_variable:feedbackMode", "state_variable:patienceLeft", "state_variable:streak",
                "state_variable:boxItems", "state_variable:conveyorItems",
                "state_variable:customerQueue", "state_variable:customerIndex",
                "constant:SUCCESS_MS", "constant:OVERSHOOT_MS",
                "callback:handlePastrySelect",
            ],
            "depends_on": ["P1-01", "P1-02", "P1-03", "P1-04", "P1-05", "P1-06", "P1-07", "P1-08", "P1-09"],
            "rationale": "BakeryRushPrototype must be built last — it owns all game state and depends on every child component and the level config data.",
        },
        {
            "patch_id": "P1-11",
            "file_path": "preview/src/App.jsx",
            "patch_type": "edit_render_output",
            "change_description": (
                "Add import for BakeryRushPrototype: import BakeryRushPrototype from './games/BakeryRushPrototype'. "
                "Replace the current active game component (or placeholder) in App's return statement "
                "with <BakeryRushPrototype />. "
                "Remove import for any previous game component that is no longer referenced."
            ),
            "location_hint": "Import block at top of file and App function return statement",
            "named_elements": ["component:BakeryRushPrototype"],
            "depends_on": ["P1-10"],
            "rationale": "App.jsx is the preview entry mount. BakeryRushPrototype must be mounted here for the preview to render the game.",
        },
    ],
    "naming_registry": [
        # Data constants
        {"name": "levelConfigs",       "name_type": "constant",        "file_path": "preview/src/games/bakery/levelConfig.js",                    "purpose": "Array of 5 level configs: speed, targets, weights, patience, scoreThreshold"},
        {"name": "PASTRY_VALUES",      "name_type": "constant",        "file_path": "preview/src/games/bakery/levelConfig.js",                    "purpose": "Maps pastry emoji to numeric math value"},
        {"name": "SUCCESS_MS",         "name_type": "constant",        "file_path": "preview/src/games/BakeryRushPrototype.jsx",                   "purpose": "Duration in ms to display success overlay before advancing"},
        {"name": "OVERSHOOT_MS",       "name_type": "constant",        "file_path": "preview/src/games/BakeryRushPrototype.jsx",                   "purpose": "Duration in ms to display overshoot feedback before bounce-back"},
        # Components
        {"name": "BakeryRushPrototype","name_type": "component",       "file_path": "preview/src/games/BakeryRushPrototype.jsx",                   "purpose": "Root game container — owns all session state and loop orchestration"},
        {"name": "OrderTicket",        "name_type": "component",       "file_path": "preview/src/games/bakery/components/OrderTicket.jsx",         "purpose": "Displays current customer, target value, and patience bar"},
        {"name": "ConveyorBelt",       "name_type": "component",       "file_path": "preview/src/games/bakery/components/ConveyorBelt.jsx",        "purpose": "Animated belt of pastry items with tap-to-select surface"},
        {"name": "PastryBox",          "name_type": "component",       "file_path": "preview/src/games/bakery/components/PastryBox.jsx",           "purpose": "Selected pastry display with running total and feedback classes"},
        {"name": "ShiftHUD",           "name_type": "component",       "file_path": "preview/src/games/bakery/components/ShiftHUD.jsx",            "purpose": "Persistent situational awareness bar: score, lives, level, queue"},
        {"name": "FeedbackOverlay",    "name_type": "component",       "file_path": "preview/src/games/bakery/components/FeedbackOverlay.jsx",     "purpose": "Full-screen feedback overlay for success, overshoot, end-of-shift"},
        # State variables (owned by BakeryRushPrototype)
        {"name": "screenState",        "name_type": "state_variable",  "file_path": "preview/src/games/BakeryRushPrototype.jsx",                   "purpose": "Top-level screen state: PLAYING or END_OF_SHIFT"},
        {"name": "levelIndex",         "name_type": "state_variable",  "file_path": "preview/src/games/BakeryRushPrototype.jsx",                   "purpose": "0-based index into levelConfigs array"},
        {"name": "score",              "name_type": "state_variable",  "file_path": "preview/src/games/BakeryRushPrototype.jsx",                   "purpose": "Cumulative session score"},
        {"name": "lives",              "name_type": "state_variable",  "file_path": "preview/src/games/BakeryRushPrototype.jsx",                   "purpose": "Remaining lives; decrements on patience expiry"},
        {"name": "currentTarget",      "name_type": "state_variable",  "file_path": "preview/src/games/BakeryRushPrototype.jsx",                   "purpose": "Target total for the current customer order"},
        {"name": "currentTotal",       "name_type": "state_variable",  "file_path": "preview/src/games/BakeryRushPrototype.jsx",                   "purpose": "Running sum of pastry values in the box"},
        {"name": "feedbackMode",       "name_type": "state_variable",  "file_path": "preview/src/games/BakeryRushPrototype.jsx",                   "purpose": "Active feedback state: success, overshoot, end_of_shift, or null"},
        {"name": "patienceLeft",       "name_type": "state_variable",  "file_path": "preview/src/games/BakeryRushPrototype.jsx",                   "purpose": "Seconds remaining before customer patience expires"},
        {"name": "streak",             "name_type": "state_variable",  "file_path": "preview/src/games/BakeryRushPrototype.jsx",                   "purpose": "Consecutive first-try successes; resets on miss or overshoot"},
        {"name": "boxItems",           "name_type": "state_variable",  "file_path": "preview/src/games/BakeryRushPrototype.jsx",                   "purpose": "Array of pastry items currently in the box"},
        {"name": "conveyorItems",      "name_type": "state_variable",  "file_path": "preview/src/games/BakeryRushPrototype.jsx",                   "purpose": "Array of pastry items currently on the conveyor belt"},
        {"name": "customerQueue",      "name_type": "state_variable",  "file_path": "preview/src/games/BakeryRushPrototype.jsx",                   "purpose": "Upcoming customer objects (emoji, name, targetValue)"},
        {"name": "customerIndex",      "name_type": "state_variable",  "file_path": "preview/src/games/BakeryRushPrototype.jsx",                   "purpose": "Index of the currently active customer in the queue"},
        # Callbacks
        {"name": "handlePastrySelect", "name_type": "callback",        "file_path": "preview/src/games/BakeryRushPrototype.jsx",                   "purpose": "Handles player tap on belt item; computes total and triggers feedback"},
        # Props (OrderTicket)
        {"name": "currentTarget",      "name_type": "prop",            "file_path": "preview/src/games/bakery/components/OrderTicket.jsx",         "purpose": "Target order total displayed in the ticket"},
        {"name": "customerName",       "name_type": "prop",            "file_path": "preview/src/games/bakery/components/OrderTicket.jsx",         "purpose": "Customer name string displayed below emoji"},
        {"name": "customerEmoji",      "name_type": "prop",            "file_path": "preview/src/games/bakery/components/OrderTicket.jsx",         "purpose": "Customer identity emoji"},
        {"name": "patiencePercent",    "name_type": "prop",            "file_path": "preview/src/games/bakery/components/OrderTicket.jsx",         "purpose": "0–1 float driving patience bar fill width"},
        {"name": "message",            "name_type": "prop",            "file_path": "preview/src/games/bakery/components/OrderTicket.jsx",         "purpose": "Optional contextual message shown below ticket"},
        # Props (ConveyorBelt)
        {"name": "items",              "name_type": "prop",            "file_path": "preview/src/games/bakery/components/ConveyorBelt.jsx",        "purpose": "Array of {id, emoji, value} pastry items to render on belt"},
        {"name": "beltDuration",       "name_type": "prop",            "file_path": "preview/src/games/bakery/components/ConveyorBelt.jsx",        "purpose": "CSS animation duration in seconds for belt-scroll"},
        {"name": "interactionEnabled", "name_type": "prop",            "file_path": "preview/src/games/bakery/components/ConveyorBelt.jsx",        "purpose": "When false, disables tap events and applies belt-item-disabled class"},
        {"name": "onPastrySelect",     "name_type": "prop",            "file_path": "preview/src/games/bakery/components/ConveyorBelt.jsx",        "purpose": "Callback invoked with the tapped item object"},
        # Props (PastryBox)
        {"name": "boxItems",           "name_type": "prop",            "file_path": "preview/src/games/bakery/components/PastryBox.jsx",           "purpose": "Array of pastry items currently in the box"},
        {"name": "currentTotal",       "name_type": "prop",            "file_path": "preview/src/games/bakery/components/PastryBox.jsx",           "purpose": "Running total value displayed in box"},
        {"name": "feedbackMode",       "name_type": "prop",            "file_path": "preview/src/games/bakery/components/PastryBox.jsx",           "purpose": "Drives box-success and box-overshoot CSS classes"},
        # Props (ShiftHUD)
        {"name": "score",              "name_type": "prop",            "file_path": "preview/src/games/bakery/components/ShiftHUD.jsx",            "purpose": "Cumulative score to display"},
        {"name": "lives",              "name_type": "prop",            "file_path": "preview/src/games/bakery/components/ShiftHUD.jsx",            "purpose": "Remaining lives count for heart display"},
        {"name": "patiencePercent",    "name_type": "prop",            "file_path": "preview/src/games/bakery/components/ShiftHUD.jsx",            "purpose": "0–1 float for patience bar fill in HUD"},
        {"name": "levelIndex",         "name_type": "prop",            "file_path": "preview/src/games/bakery/components/ShiftHUD.jsx",            "purpose": "0-based level index for level badge display"},
        {"name": "queue",              "name_type": "prop",            "file_path": "preview/src/games/bakery/components/ShiftHUD.jsx",            "purpose": "Array of upcoming customer preview objects for queue strip"},
        # Props (FeedbackOverlay)
        {"name": "feedbackMode",       "name_type": "prop",            "file_path": "preview/src/games/bakery/components/FeedbackOverlay.jsx",     "purpose": "Controls overlay visibility and variant (success/overshoot/end_of_shift/null)"},
        {"name": "customerReaction",   "name_type": "prop",            "file_path": "preview/src/games/bakery/components/FeedbackOverlay.jsx",     "purpose": "Emoji shown in overlay-emoji for the current feedback state"},
        {"name": "summaryStats",       "name_type": "prop",            "file_path": "preview/src/games/bakery/components/FeedbackOverlay.jsx",     "purpose": "Object with score, ordersCompleted, streakBest for end-of-shift display"},
        # CSS classes
        {"name": "bakery-rush",        "name_type": "css_class",       "file_path": "preview/src/games/bakery/styles.css",                        "purpose": "Root game wrapper: flex column, 100vh, base font"},
        {"name": "conveyor-belt",      "name_type": "css_class",       "file_path": "preview/src/games/bakery/styles.css",                        "purpose": "Overflow-hidden container for the belt track"},
        {"name": "belt-track",         "name_type": "css_class",       "file_path": "preview/src/games/bakery/styles.css",                        "purpose": "Flex row that scrolls via belt-scroll animation"},
        {"name": "belt-item",          "name_type": "css_class",       "file_path": "preview/src/games/bakery/styles.css",                        "purpose": "Individual tappable pastry item on the belt"},
        {"name": "belt-item-disabled", "name_type": "css_class",       "file_path": "preview/src/games/bakery/styles.css",                        "purpose": "Applied when interactionEnabled is false"},
        {"name": "pastry-emoji",       "name_type": "css_class",       "file_path": "preview/src/games/bakery/styles.css",                        "purpose": "Large emoji span on belt item"},
        {"name": "pastry-value",       "name_type": "css_class",       "file_path": "preview/src/games/bakery/styles.css",                        "purpose": "Small +N value label below emoji on belt item"},
        {"name": "patience-bar",       "name_type": "css_class",       "file_path": "preview/src/games/bakery/styles.css",                        "purpose": "Track div for patience fill in OrderTicket"},
        {"name": "patience-fill",      "name_type": "css_class",       "file_path": "preview/src/games/bakery/styles.css",                        "purpose": "Fill div inside patience-bar, width driven by patiencePercent"},
        {"name": "hud-patience-bar",   "name_type": "css_class",       "file_path": "preview/src/games/bakery/styles.css",                        "purpose": "Track div for patience fill in ShiftHUD"},
        {"name": "hud-patience-fill",  "name_type": "css_class",       "file_path": "preview/src/games/bakery/styles.css",                        "purpose": "Fill div inside hud-patience-bar"},
        {"name": "pastry-box",         "name_type": "css_class",       "file_path": "preview/src/games/bakery/styles.css",                        "purpose": "Box container with border; receives success/overshoot modifier classes"},
        {"name": "box-success",        "name_type": "css_class",       "file_path": "preview/src/games/bakery/styles.css",                        "purpose": "Green glow applied on exact match"},
        {"name": "box-overshoot",      "name_type": "css_class",       "file_path": "preview/src/games/bakery/styles.css",                        "purpose": "Shake animation applied on overshoot"},
        {"name": "box-items-grid",     "name_type": "css_class",       "file_path": "preview/src/games/bakery/styles.css",                        "purpose": "Wrapping grid for box item emoji chips"},
        {"name": "box-item",           "name_type": "css_class",       "file_path": "preview/src/games/bakery/styles.css",                        "purpose": "Single emoji chip inside the pastry box"},
        {"name": "box-total-row",      "name_type": "css_class",       "file_path": "preview/src/games/bakery/styles.css",                        "purpose": "Row containing total label and value"},
        {"name": "box-total-label",    "name_type": "css_class",       "file_path": "preview/src/games/bakery/styles.css",                        "purpose": "'Total:' label in total row"},
        {"name": "box-total-value",    "name_type": "css_class",       "file_path": "preview/src/games/bakery/styles.css",                        "purpose": "Bold current total number in total row"},
        {"name": "box-target-label",   "name_type": "css_class",       "file_path": "preview/src/games/bakery/styles.css",                        "purpose": "'of N' target indicator below total"},
        {"name": "feedback-overlay",   "name_type": "css_class",       "file_path": "preview/src/games/bakery/styles.css",                        "purpose": "Fixed inset-0 overlay; base class for all overlay variants"},
        {"name": "overlay-success",    "name_type": "css_class",       "file_path": "preview/src/games/bakery/styles.css",                        "purpose": "Green background overlay for exact match"},
        {"name": "overlay-overshoot",  "name_type": "css_class",       "file_path": "preview/src/games/bakery/styles.css",                        "purpose": "Red background overlay for overshoot"},
        {"name": "overlay-end",        "name_type": "css_class",       "file_path": "preview/src/games/bakery/styles.css",                        "purpose": "Blue background overlay for end-of-shift summary"},
        {"name": "overlay-inner",      "name_type": "css_class",       "file_path": "preview/src/games/bakery/styles.css",                        "purpose": "Centered content wrapper inside overlay"},
        {"name": "overlay-emoji",      "name_type": "css_class",       "file_path": "preview/src/games/bakery/styles.css",                        "purpose": "Large reaction emoji inside overlay"},
        {"name": "overlay-title",      "name_type": "css_class",       "file_path": "preview/src/games/bakery/styles.css",                        "purpose": "Bold title text inside overlay"},
        {"name": "overlay-subtitle",   "name_type": "css_class",       "file_path": "preview/src/games/bakery/styles.css",                        "purpose": "Secondary message text inside overlay"},
        {"name": "overlay-stats",      "name_type": "css_class",       "file_path": "preview/src/games/bakery/styles.css",                        "purpose": "Summary stats block visible in end-of-shift overlay"},
        {"name": "shift-hud",          "name_type": "css_class",       "file_path": "preview/src/games/bakery/styles.css",                        "purpose": "HUD strip at top of game: score, lives, level, queue"},
        {"name": "hud-score-label",    "name_type": "css_class",       "file_path": "preview/src/games/bakery/styles.css",                        "purpose": "'Score' label in HUD"},
        {"name": "hud-score-value",    "name_type": "css_class",       "file_path": "preview/src/games/bakery/styles.css",                        "purpose": "Score number in HUD"},
        {"name": "hud-lives",          "name_type": "css_class",       "file_path": "preview/src/games/bakery/styles.css",                        "purpose": "Heart emoji row in HUD"},
        {"name": "hud-level-badge",    "name_type": "css_class",       "file_path": "preview/src/games/bakery/styles.css",                        "purpose": "Pill badge showing current level"},
        {"name": "hud-queue",          "name_type": "css_class",       "file_path": "preview/src/games/bakery/styles.css",                        "purpose": "Queue preview strip in HUD"},
        {"name": "hud-queue-item",     "name_type": "css_class",       "file_path": "preview/src/games/bakery/styles.css",                        "purpose": "Single upcoming customer chip in queue"},
        {"name": "order-ticket",       "name_type": "css_class",       "file_path": "preview/src/games/bakery/styles.css",                        "purpose": "Outer wrapper for OrderTicket card"},
        {"name": "order-target-label", "name_type": "css_class",       "file_path": "preview/src/games/bakery/styles.css",                        "purpose": "'Order' label above target number"},
        {"name": "order-target-value", "name_type": "css_class",       "file_path": "preview/src/games/bakery/styles.css",                        "purpose": "Large bold target number in ticket"},
        {"name": "order-message",      "name_type": "css_class",       "file_path": "preview/src/games/bakery/styles.css",                        "purpose": "Contextual message paragraph below ticket"},
        # CSS custom properties
        {"name": "--belt-duration",    "name_type": "css_custom_property", "file_path": "preview/src/games/bakery/styles.css",                    "purpose": "CSS animation duration for belt-scroll, set inline from beltDuration prop"},
        # Keyframes
        {"name": "belt-scroll",        "name_type": "keyframe",        "file_path": "preview/src/games/bakery/styles.css",                        "purpose": "Continuous left-scroll animation for conveyor belt track"},
        {"name": "box-shake",          "name_type": "keyframe",        "file_path": "preview/src/games/bakery/styles.css",                        "purpose": "Horizontal rejection shake on overshoot"},
        {"name": "overlay-enter",      "name_type": "keyframe",        "file_path": "preview/src/games/bakery/styles.css",                        "purpose": "Scale-in entry animation for feedback overlay"},
    ],
    "animation_contracts": [
        {
            "animation_id": "belt-scroll",
            "trigger": "ConveyorBelt mounts and interactionEnabled is true",
            "duration_ms": 4000,
            "easing": "linear",
            "css_custom_properties": ["--belt-duration"],
            "keyframe_name": "belt-scroll",
            "owner_file": "preview/src/games/bakery/styles.css",
            "element_selector": ".belt-track",
            "dom_measurement_required": False,
        },
        {
            "animation_id": "box-shake",
            "trigger": "box-overshoot class applied when currentTotal > currentTarget",
            "duration_ms": 350,
            "easing": "ease",
            "css_custom_properties": [],
            "keyframe_name": "box-shake",
            "owner_file": "preview/src/games/bakery/styles.css",
            "element_selector": ".pastry-box.box-overshoot",
            "dom_measurement_required": False,
        },
        {
            "animation_id": "overlay-enter",
            "trigger": "FeedbackOverlay renders (feedbackMode is non-null)",
            "duration_ms": 180,
            "easing": "cubic-bezier(0.17, 0.89, 0.32, 1.1)",
            "css_custom_properties": [],
            "keyframe_name": "overlay-enter",
            "owner_file": "preview/src/games/bakery/styles.css",
            "element_selector": ".feedback-overlay",
            "dom_measurement_required": False,
        },
    ],
    "acceptance_signals": [
        {
            "signal_id": "AS1-01",
            "description": "Conveyor belt scrolls continuously with pastry items",
            "observable_in_browser": "Belt items move left continuously at a readable speed on Level 1",
            "related_patches": ["P1-03", "P1-04", "P1-06"],
        },
        {
            "signal_id": "AS1-02",
            "description": "Tapping a pastry adds it to the box and increments the total",
            "observable_in_browser": "Tap on any belt item → emoji appears in pastry box → running total increases by item value",
            "related_patches": ["P1-06", "P1-07", "P1-10"],
        },
        {
            "signal_id": "AS1-03",
            "description": "Exact match triggers success overlay",
            "observable_in_browser": "When currentTotal === currentTarget, green overlay appears with emoji and 'Perfect order!' message",
            "related_patches": ["P1-09", "P1-10"],
        },
        {
            "signal_id": "AS1-04",
            "description": "Overshoot triggers shake and bounce-back",
            "observable_in_browser": "When total exceeds target, box shakes, overshoot overlay appears briefly, total resets",
            "related_patches": ["P1-03", "P1-04", "P1-07", "P1-09", "P1-10"],
        },
        {
            "signal_id": "AS1-05",
            "description": "Patience bar depletes and causes a miss",
            "observable_in_browser": "Bar empties in real time; when fully empty, lives decrement and next customer loads",
            "related_patches": ["P1-05", "P1-08", "P1-10"],
        },
        {
            "signal_id": "AS1-06",
            "description": "Level badge increments on score threshold",
            "observable_in_browser": "HUD shows 'Lv 2' after score crosses Level 1 scoreThreshold; belt speed visibly increases",
            "related_patches": ["P1-01", "P1-08", "P1-10"],
        },
    ],
    "patch_notes": (
        "Pass 1 creates the full file structure declared in implementation_plan.file_plan. "
        "All state lives in BakeryRushPrototype — no child component owns gameplay logic. "
        "The conveyor belt renders items twice (items.concat(items)) so the CSS scroll loop is seamless. "
        "Belt speed is communicated to CSS via --belt-duration custom property; "
        "beltDuration in seconds = track width / conveyorSpeed — derive this in BakeryRushPrototype before passing to ConveyorBelt. "
        "OVERSHOOT_MS must elapse before currentTotal is decremented — the shake animation must complete first. "
        "Patience timer must be cleared (clearInterval) whenever feedbackMode becomes non-null, "
        "and restarted when the next customer loads."
    ),
}

# ---------------------------------------------------------------------------
# Fire Station Dispatch — route_and_dispatch interaction — Pass 1
# ---------------------------------------------------------------------------

_FIRE_DISPATCH_PATCH_PLAN: Dict[str, Any] = {
    "patch_objective": (
        "Create the initial playable Fire Station Dispatch prototype: mission config data, "
        "four UI components (MissionCard, TruckYard, DispatchBoard, OutcomeOverlay), "
        "styles, and the FireDispatchPrototype root container with full dispatch state and loop logic."
    ),
    "source_pass": {
        "pass_number": 1,
        "pass_label": "Core Dispatch Loop",
        "features_added": [
            "Level config data: 5 levels with incidentTypes, truckTypes, timeLimit, scoreThreshold",
            "MissionCard component: shows incident name, location, and arithmetic demand value",
            "TruckYard component: renders tap-to-toggle trucks with capacity labels",
            "DispatchBoard component: shows dispatched trucks and running capacity total vs demand",
            "OutcomeOverlay component: full-screen success, excess, timeout, and shift-end states",
            "FireDispatchPrototype: root container with full dispatch state, timer, and loop orchestration",
        ],
    },
    "target_files": [
        {
            "file_path": "preview/src/App.jsx",
            "operation": "edit",
            "current_state": "Mounts previous game component or placeholder",
            "post_patch_state": "Mounts FireDispatchPrototype as the active game component",
        },
        {
            "file_path": "preview/src/games/FireDispatchPrototype.jsx",
            "operation": "create",
            "current_state": "File does not exist",
            "post_patch_state": "Root container with dispatch state, incident queue, timer, and child wiring",
        },
        {
            "file_path": "preview/src/games/fire/missionConfig.js",
            "operation": "create",
            "current_state": "File does not exist",
            "post_patch_state": "Exports LEVEL_CONFIGS array and TRUCK_TYPES constant",
        },
        {
            "file_path": "preview/src/games/fire/components/MissionCard.jsx",
            "operation": "create",
            "current_state": "File does not exist",
            "post_patch_state": "Presentational card showing incident type, location, and demand value",
        },
        {
            "file_path": "preview/src/games/fire/components/TruckYard.jsx",
            "operation": "create",
            "current_state": "File does not exist",
            "post_patch_state": "Tap-to-toggle truck grid with capacity labels and selection state",
        },
        {
            "file_path": "preview/src/games/fire/components/DispatchBoard.jsx",
            "operation": "create",
            "current_state": "File does not exist",
            "post_patch_state": "Running capacity total vs demand display with dispatched truck indicators",
        },
        {
            "file_path": "preview/src/games/fire/components/OutcomeOverlay.jsx",
            "operation": "create",
            "current_state": "File does not exist",
            "post_patch_state": "Full-screen overlay for SUCCESS, EXCESS, TIMEOUT, and SHIFT_END states",
        },
        {
            "file_path": "preview/src/games/fire/styles.css",
            "operation": "create",
            "current_state": "File does not exist",
            "post_patch_state": "All layout, motion, and readability styles scoped to .fire-dispatch class",
        },
    ],
    "patch_sequence": [
        {
            "patch_id": "P1-01",
            "file_path": "preview/src/games/fire/missionConfig.js",
            "patch_type": "add_constant",
            "change_description": (
                "Export LEVEL_CONFIGS as the default export — array of 5 level objects. "
                "Each level: incidentTypes (array of {name, emoji, location, demandValue}), "
                "truckTypes (array of {id, emoji, label, capacity}), "
                "timeLimit (integer seconds), scoreThreshold (integer), streakBonus (integer). "
                "Level 1: timeLimit 25, demandValues 4–8, 2 truck types. "
                "Level 2: timeLimit 20, demandValues 5–12, 3 truck types. "
                "Level 3: timeLimit 18, demandValues 6–15, 3 truck types. "
                "Level 4: timeLimit 15, demandValues 8–18, 4 truck types. "
                "Level 5: timeLimit 12, demandValues 10–20, 4 truck types."
            ),
            "location_hint": "Top of file, default export",
            "named_elements": ["constant:LEVEL_CONFIGS"],
            "depends_on": [],
            "rationale": "All incident and truck definitions must be data-driven and separate from component logic.",
        },
        {
            "patch_id": "P1-02",
            "file_path": "preview/src/games/fire/missionConfig.js",
            "patch_type": "add_constant",
            "change_description": (
                "Export TRUCK_TYPES as a named const array of canonical truck definitions used across all levels. "
                "Each entry: {id, emoji, label, capacity}. "
                "Entries: hose_truck (🚒, capacity 5), ladder_truck (🪜, capacity 3), "
                "ambulance (🚑, capacity 2), command_vehicle (🚐, capacity 4), water_tanker (🚛, capacity 6). "
                "Levels reference these by id and override capacity for difficulty scaling."
            ),
            "location_hint": "After LEVEL_CONFIGS default export",
            "named_elements": ["constant:TRUCK_TYPES"],
            "depends_on": ["P1-01"],
            "rationale": "Canonical truck types prevent duplication across level config entries.",
        },
        {
            "patch_id": "P1-03",
            "file_path": "preview/src/games/fire/styles.css",
            "patch_type": "add_css_class",
            "change_description": (
                "Create the full stylesheet for Fire Dispatch. "
                "Root: .fire-dispatch (flex column, 100vh, background #1a1a2e, color #fff, font-family sans-serif). "
                "Mission card: .mission-card (background #16213e, border-radius 12px, padding 20px). "
                ".mission-emoji (font-size 3rem, display block). "
                ".mission-name (font-size 1.4rem, font-weight 700). "
                ".mission-location (font-size 0.9rem, opacity 0.7). "
                ".demand-label (font-size 0.75rem, uppercase, letter-spacing 0.08em, opacity 0.6). "
                ".demand-value (font-size 4rem, font-weight 900, color #f59e0b). "
                "Truck yard: .truck-yard (display flex, flex-wrap wrap, gap 12px, padding 16px). "
                ".truck-card (flex column, align-items center, padding 12px 16px, background #16213e, "
                "border 2px solid transparent, border-radius 12px, cursor pointer, transition 0.15s). "
                ".truck-selected (border-color #22c55e, background #1a3a2a, animation truck-bounce 0.3s ease). "
                ".truck-emoji (font-size 2.5rem). "
                ".truck-capacity (font-size 0.85rem, font-weight 700, color #94a3b8). "
                "Dispatch board: .dispatch-board (background #16213e, border-radius 12px, padding 16px). "
                ".board-trucks (display flex, gap 8px, flex-wrap wrap). "
                ".board-truck (font-size 1.8rem). "
                ".board-total (font-size 3rem, font-weight 900, color #22c55e). "
                ".board-demand (font-size 1rem, opacity 0.6). "
                ".board-excess (.board-total color #ef4444). "
                "Timer: .timer-bar (height 6px, background rgba(255,255,255,0.15), border-radius 3px). "
                ".timer-fill (height 100%, background #f59e0b, border-radius 3px, transition width 0.3s linear). "
                ".timer-urgent (.timer-fill background #ef4444, animation timer-pulse 0.5s ease infinite). "
                "HUD: .dispatch-hud (display flex, align-items center, gap 16px, padding 12px 16px, "
                "background rgba(0,0,0,0.3)). "
                "Overlay: .outcome-overlay (position fixed, inset 0, z-index 50, display flex, align-items center, "
                "justify-content center, animation overlay-enter 0.2s cubic-bezier(0.17,0.89,0.32,1.1) forwards). "
                ".overlay-success (background rgba(22,163,74,0.93)). "
                ".overlay-excess (background rgba(220,38,38,0.9)). "
                ".overlay-timeout (background rgba(180,83,9,0.9)). "
                ".overlay-end (background rgba(30,30,80,0.95)). "
                ".overlay-inner (text-align center, color #fff). "
                ".overlay-emoji (font-size 5rem, display block). "
                ".overlay-title (font-size 2rem, font-weight 800, margin-top 12px). "
                ".overlay-subtitle (font-size 1.1rem, margin-top 8px, opacity 0.9)."
            ),
            "location_hint": "Full file content — new file",
            "named_elements": [
                "css_class:fire-dispatch",
                "css_class:mission-card", "css_class:mission-emoji", "css_class:mission-name",
                "css_class:mission-location", "css_class:demand-label", "css_class:demand-value",
                "css_class:truck-yard", "css_class:truck-card", "css_class:truck-selected",
                "css_class:truck-emoji", "css_class:truck-capacity",
                "css_class:dispatch-board", "css_class:board-trucks", "css_class:board-truck",
                "css_class:board-total", "css_class:board-demand", "css_class:board-excess",
                "css_class:timer-bar", "css_class:timer-fill", "css_class:timer-urgent",
                "css_class:dispatch-hud",
                "css_class:outcome-overlay", "css_class:overlay-success", "css_class:overlay-excess",
                "css_class:overlay-timeout", "css_class:overlay-end",
                "css_class:overlay-inner", "css_class:overlay-emoji",
                "css_class:overlay-title", "css_class:overlay-subtitle",
            ],
            "depends_on": [],
            "rationale": "All shared animation classes and layout primitives must exist before any component imports the stylesheet.",
        },
        {
            "patch_id": "P1-04",
            "file_path": "preview/src/games/fire/styles.css",
            "patch_type": "add_keyframe",
            "change_description": (
                "Add four keyframes. "
                "truck-bounce: 0% scale(1), 40% scale(1.2) translateY(-4px), 100% scale(1) — "
                "snappy bounce when a truck is selected. "
                "dispatch-shake: 0%/100% translateX(0), 20% translateX(-6px), 60% translateX(6px) — "
                "horizontal rejection for excess dispatch. "
                "overlay-enter: from (opacity 0, scale(0.9)) to (opacity 1, scale(1)) — "
                "scale-in entry for outcome overlay. "
                "timer-pulse: 0%/100% opacity 1, 50% opacity 0.4 — "
                "urgent blink applied when timeLeft < 5."
            ),
            "location_hint": "After all CSS class rules, end of file",
            "named_elements": [
                "keyframe:truck-bounce", "keyframe:dispatch-shake",
                "keyframe:overlay-enter", "keyframe:timer-pulse",
            ],
            "depends_on": ["P1-03"],
            "rationale": "Keyframes must be in the same file as the classes that reference them.",
        },
        {
            "patch_id": "P1-05",
            "file_path": "preview/src/games/fire/components/MissionCard.jsx",
            "patch_type": "add_component",
            "change_description": (
                "Create MissionCard as a default export function. "
                "Props: incidentName (string), incidentEmoji (string), locationName (string), "
                "demandValue (number), urgency (string: 'low'|'medium'|'high'). "
                "Render: outer div class mission-card. "
                "Header: mission-emoji span, mission-name h2. "
                "Location: mission-location p ('📍 ' + locationName). "
                "Demand display: demand-label div ('Trucks needed:'), demand-value div (demandValue as large number). "
                "Urgency indicator: a span with text matching urgency level."
            ),
            "location_hint": "Full file content — new file",
            "named_elements": [
                "component:MissionCard",
                "prop:incidentName", "prop:incidentEmoji", "prop:locationName",
                "prop:demandValue", "prop:urgency",
            ],
            "depends_on": ["P1-03"],
            "rationale": "MissionCard is purely presentational — all incident data flows in as props.",
        },
        {
            "patch_id": "P1-06",
            "file_path": "preview/src/games/fire/components/TruckYard.jsx",
            "patch_type": "add_component",
            "change_description": (
                "Create TruckYard as a default export function. "
                "Props: trucks (array of {id, emoji, label, capacity}), "
                "selectedIds (Set of selected truck ids), "
                "dispatchEnabled (boolean), onTruckToggle (function(truckId) => void). "
                "Render: outer div class truck-yard. "
                "Map trucks to truck-card divs. "
                "Apply truck-selected class when truck.id is in selectedIds. "
                "Each card: truck-emoji span, label p, truck-capacity span ('+' + truck.capacity). "
                "On click: call onTruckToggle(truck.id) only when dispatchEnabled is true. "
                "Add role='button', tabIndex=0 for keyboard access."
            ),
            "location_hint": "Full file content — new file",
            "named_elements": [
                "component:TruckYard",
                "prop:trucks", "prop:selectedIds", "prop:dispatchEnabled", "prop:onTruckToggle",
            ],
            "depends_on": ["P1-03"],
            "rationale": "TruckYard is a stateless multi-select surface — selection state lives in the root container.",
        },
        {
            "patch_id": "P1-07",
            "file_path": "preview/src/games/fire/components/DispatchBoard.jsx",
            "patch_type": "add_component",
            "change_description": (
                "Create DispatchBoard as a default export function. "
                "Props: selectedTrucks (array of dispatched truck objects), "
                "totalCapacity (number), demandValue (number), feedbackMode (string|null). "
                "Render: outer div class dispatch-board. "
                "Dispatched trucks row: board-trucks div mapping selectedTrucks to board-truck spans (emoji only). "
                "Total display: board-total div (totalCapacity as large number). "
                "Apply board-excess modifier when feedbackMode === 'excess'. "
                "Demand context: board-demand div ('of ' + demandValue + ' needed'). "
                "Apply dispatch-shake animation (via CSS class excess-shake) when feedbackMode is 'excess'."
            ),
            "location_hint": "Full file content — new file",
            "named_elements": [
                "component:DispatchBoard",
                "prop:selectedTrucks", "prop:totalCapacity", "prop:demandValue", "prop:feedbackMode",
            ],
            "depends_on": ["P1-03"],
            "rationale": "DispatchBoard makes the arithmetic visible — running total vs demand at all times.",
        },
        {
            "patch_id": "P1-08",
            "file_path": "preview/src/games/fire/components/OutcomeOverlay.jsx",
            "patch_type": "add_component",
            "change_description": (
                "Create OutcomeOverlay as a default export function. "
                "Props: feedbackMode (string|null: 'success'|'excess'|'timeout'|'shift_end'|null), "
                "summaryStats ({score, incidentsResolved, streakBest}). "
                "Returns null when feedbackMode is null. "
                "Render: outer div class outcome-overlay plus variant class (overlay-success, overlay-excess, "
                "overlay-timeout, overlay-end based on feedbackMode). "
                "Inner: overlay-inner div with overlay-emoji (appropriate emoji), "
                "overlay-title (state label), overlay-subtitle (contextual message). "
                "When feedbackMode is 'shift_end': also render overlay-stats div with score, "
                "incidentsResolved, and streakBest from summaryStats."
            ),
            "location_hint": "Full file content — new file",
            "named_elements": [
                "component:OutcomeOverlay",
                "prop:feedbackMode", "prop:summaryStats",
            ],
            "depends_on": ["P1-03"],
            "rationale": "OutcomeOverlay is a stateless conditional renderer — feedbackMode is the single switch.",
        },
        {
            "patch_id": "P1-09",
            "file_path": "preview/src/games/FireDispatchPrototype.jsx",
            "patch_type": "add_component",
            "change_description": (
                "Create FireDispatchPrototype as a default export function. "
                "Imports: LEVEL_CONFIGS, TRUCK_TYPES from './fire/missionConfig'. "
                "Imports: MissionCard, TruckYard, DispatchBoard, OutcomeOverlay from './fire/components/'. "
                "Imports: './fire/styles.css'. "
                "Module constants: SUCCESS_MS = 1400, EXCESS_MS = 800, TIMEOUT_MS = 1200. "
                "State (all via useState): levelIndex (0), score (0), lives (3), "
                "incidents (generated from LEVEL_CONFIGS[0].incidentTypes), "
                "incidentIndex (0), dispatched ([] array of selected trucks), "
                "totalCapacity (0), feedbackMode (null), timeLeft (LEVEL_CONFIGS[0].timeLimit), "
                "streak (0), sessionComplete (false). "
                "Derived: currentLevel = LEVEL_CONFIGS[levelIndex], "
                "currentIncident = incidents[incidentIndex], "
                "availableTrucks = currentLevel.truckTypes, "
                "timePercent = timeLeft / currentLevel.timeLimit. "
                "Timer useEffect: decrements timeLeft by 1 each second when feedbackMode is null. "
                "On timeLeft reaching 0: decrement lives, set feedbackMode 'timeout'. "
                "After TIMEOUT_MS: advance incident, reset dispatch state. "
                "On lives reaching 0: set sessionComplete true, feedbackMode 'shift_end'. "
                "handleTruckToggle(truckId): toggle truckId in dispatched array; "
                "recompute totalCapacity as sum of dispatched truck capacities. "
                "handleDispatch(): if feedbackMode non-null return. "
                "If totalCapacity === currentIncident.demandValue: award score, increment streak, "
                "set feedbackMode 'success'. After SUCCESS_MS: advance incident, reset dispatch. "
                "If totalCapacity > currentIncident.demandValue: set feedbackMode 'excess'. "
                "After EXCESS_MS: clear feedbackMode only (keep dispatch state for correction). "
                "Level advance: when score >= currentLevel.scoreThreshold and levelIndex < 4: increment levelIndex. "
                "Render: root div class fire-dispatch. "
                "Always: OutcomeOverlay (feedbackMode, summaryStats). "
                "When not sessionComplete: timer-bar with timer-fill (width = timePercent * 100%), "
                "MissionCard (currentIncident props), TruckYard (availableTrucks, dispatched ids, dispatch enabled when feedbackMode null, handleTruckToggle), "
                "DispatchBoard (dispatched trucks, totalCapacity, currentIncident.demandValue, feedbackMode), "
                "Dispatch button that calls handleDispatch."
            ),
            "location_hint": "Full file content — new file",
            "named_elements": [
                "component:FireDispatchPrototype",
                "state_variable:levelIndex", "state_variable:score", "state_variable:lives",
                "state_variable:incidents", "state_variable:incidentIndex",
                "state_variable:dispatched", "state_variable:totalCapacity",
                "state_variable:feedbackMode", "state_variable:timeLeft",
                "state_variable:streak", "state_variable:sessionComplete",
                "constant:SUCCESS_MS", "constant:EXCESS_MS", "constant:TIMEOUT_MS",
                "callback:handleTruckToggle", "callback:handleDispatch",
            ],
            "depends_on": ["P1-01", "P1-02", "P1-03", "P1-04", "P1-05", "P1-06", "P1-07", "P1-08"],
            "rationale": "Root container must be built last — it depends on all child components and the level config data.",
        },
        {
            "patch_id": "P1-10",
            "file_path": "preview/src/App.jsx",
            "patch_type": "edit_render_output",
            "change_description": (
                "Add import for FireDispatchPrototype: import FireDispatchPrototype from './games/FireDispatchPrototype'. "
                "Replace the current active game component in App's return statement with <FireDispatchPrototype />. "
                "Remove import for any previous game component no longer referenced."
            ),
            "location_hint": "Import block at top of file and App function return statement",
            "named_elements": ["component:FireDispatchPrototype"],
            "depends_on": ["P1-09"],
            "rationale": "App.jsx is the preview entry mount. FireDispatchPrototype must be mounted here for the preview to render.",
        },
    ],
    "naming_registry": [
        {"name": "LEVEL_CONFIGS",          "name_type": "constant",        "file_path": "preview/src/games/fire/missionConfig.js",                    "purpose": "Array of 5 level configs: incident types, truck types, time limit, score threshold"},
        {"name": "TRUCK_TYPES",            "name_type": "constant",        "file_path": "preview/src/games/fire/missionConfig.js",                    "purpose": "Canonical truck definitions with emoji, label, and capacity"},
        {"name": "SUCCESS_MS",             "name_type": "constant",        "file_path": "preview/src/games/FireDispatchPrototype.jsx",                 "purpose": "Duration in ms to show success overlay before advancing"},
        {"name": "EXCESS_MS",              "name_type": "constant",        "file_path": "preview/src/games/FireDispatchPrototype.jsx",                 "purpose": "Duration in ms to show excess feedback before allowing correction"},
        {"name": "TIMEOUT_MS",             "name_type": "constant",        "file_path": "preview/src/games/FireDispatchPrototype.jsx",                 "purpose": "Duration in ms to show timeout overlay before advancing"},
        {"name": "FireDispatchPrototype",  "name_type": "component",       "file_path": "preview/src/games/FireDispatchPrototype.jsx",                 "purpose": "Root game container — owns all dispatch state and loop orchestration"},
        {"name": "MissionCard",            "name_type": "component",       "file_path": "preview/src/games/fire/components/MissionCard.jsx",          "purpose": "Shows active incident type, location, and arithmetic demand value"},
        {"name": "TruckYard",              "name_type": "component",       "file_path": "preview/src/games/fire/components/TruckYard.jsx",            "purpose": "Tap-to-toggle truck selection grid with capacity labels"},
        {"name": "DispatchBoard",          "name_type": "component",       "file_path": "preview/src/games/fire/components/DispatchBoard.jsx",        "purpose": "Running capacity total vs demand with dispatched truck display"},
        {"name": "OutcomeOverlay",         "name_type": "component",       "file_path": "preview/src/games/fire/components/OutcomeOverlay.jsx",       "purpose": "Full-screen outcome feedback for success, excess, timeout, shift-end"},
        {"name": "levelIndex",             "name_type": "state_variable",  "file_path": "preview/src/games/FireDispatchPrototype.jsx",                 "purpose": "0-based index into LEVEL_CONFIGS"},
        {"name": "score",                  "name_type": "state_variable",  "file_path": "preview/src/games/FireDispatchPrototype.jsx",                 "purpose": "Cumulative session score"},
        {"name": "lives",                  "name_type": "state_variable",  "file_path": "preview/src/games/FireDispatchPrototype.jsx",                 "purpose": "Remaining lives; decrements on timeout"},
        {"name": "incidents",              "name_type": "state_variable",  "file_path": "preview/src/games/FireDispatchPrototype.jsx",                 "purpose": "Array of incident objects for current level"},
        {"name": "incidentIndex",          "name_type": "state_variable",  "file_path": "preview/src/games/FireDispatchPrototype.jsx",                 "purpose": "Index of the current active incident"},
        {"name": "dispatched",             "name_type": "state_variable",  "file_path": "preview/src/games/FireDispatchPrototype.jsx",                 "purpose": "Array of selected truck objects for the current dispatch"},
        {"name": "totalCapacity",          "name_type": "state_variable",  "file_path": "preview/src/games/FireDispatchPrototype.jsx",                 "purpose": "Sum of dispatched truck capacities — the running arithmetic total"},
        {"name": "feedbackMode",           "name_type": "state_variable",  "file_path": "preview/src/games/FireDispatchPrototype.jsx",                 "purpose": "Active feedback state: success, excess, timeout, shift_end, or null"},
        {"name": "timeLeft",               "name_type": "state_variable",  "file_path": "preview/src/games/FireDispatchPrototype.jsx",                 "purpose": "Seconds remaining for the current incident"},
        {"name": "streak",                 "name_type": "state_variable",  "file_path": "preview/src/games/FireDispatchPrototype.jsx",                 "purpose": "Consecutive first-try correct dispatches"},
        {"name": "sessionComplete",        "name_type": "state_variable",  "file_path": "preview/src/games/FireDispatchPrototype.jsx",                 "purpose": "True when lives reach 0, triggering end-of-shift summary"},
        {"name": "handleTruckToggle",      "name_type": "callback",        "file_path": "preview/src/games/FireDispatchPrototype.jsx",                 "purpose": "Toggles a truck in the dispatched array and updates totalCapacity"},
        {"name": "handleDispatch",         "name_type": "callback",        "file_path": "preview/src/games/FireDispatchPrototype.jsx",                 "purpose": "Evaluates totalCapacity vs demandValue and triggers success or excess"},
        {"name": "incidentName",           "name_type": "prop",            "file_path": "preview/src/games/fire/components/MissionCard.jsx",          "purpose": "Incident name string displayed in mission card title"},
        {"name": "incidentEmoji",          "name_type": "prop",            "file_path": "preview/src/games/fire/components/MissionCard.jsx",          "purpose": "Incident type emoji displayed large in mission card"},
        {"name": "locationName",           "name_type": "prop",            "file_path": "preview/src/games/fire/components/MissionCard.jsx",          "purpose": "Location string shown with pin emoji below incident name"},
        {"name": "demandValue",            "name_type": "prop",            "file_path": "preview/src/games/fire/components/MissionCard.jsx",          "purpose": "Arithmetic target — total truck capacity required to resolve the incident"},
        {"name": "urgency",                "name_type": "prop",            "file_path": "preview/src/games/fire/components/MissionCard.jsx",          "purpose": "Urgency level string driving visual cue (low/medium/high)"},
        {"name": "trucks",                 "name_type": "prop",            "file_path": "preview/src/games/fire/components/TruckYard.jsx",            "purpose": "Available truck objects array to display in the yard"},
        {"name": "selectedIds",            "name_type": "prop",            "file_path": "preview/src/games/fire/components/TruckYard.jsx",            "purpose": "Set of currently selected truck ids for visual state"},
        {"name": "dispatchEnabled",        "name_type": "prop",            "file_path": "preview/src/games/fire/components/TruckYard.jsx",            "purpose": "False during feedback windows to prevent input"},
        {"name": "onTruckToggle",          "name_type": "prop",            "file_path": "preview/src/games/fire/components/TruckYard.jsx",            "purpose": "Callback to toggle truck selection in root state"},
        {"name": "selectedTrucks",         "name_type": "prop",            "file_path": "preview/src/games/fire/components/DispatchBoard.jsx",        "purpose": "Array of selected truck objects to display as dispatched"},
        {"name": "summaryStats",           "name_type": "prop",            "file_path": "preview/src/games/fire/components/OutcomeOverlay.jsx",       "purpose": "Session summary data displayed in shift-end state"},
        {"name": "fire-dispatch",          "name_type": "css_class",       "file_path": "preview/src/games/fire/styles.css",                          "purpose": "Root game wrapper: dark theme flex column"},
        {"name": "mission-card",           "name_type": "css_class",       "file_path": "preview/src/games/fire/styles.css",                          "purpose": "Incident display card container"},
        {"name": "mission-emoji",          "name_type": "css_class",       "file_path": "preview/src/games/fire/styles.css",                          "purpose": "Large incident type emoji"},
        {"name": "mission-name",           "name_type": "css_class",       "file_path": "preview/src/games/fire/styles.css",                          "purpose": "Incident name heading"},
        {"name": "mission-location",       "name_type": "css_class",       "file_path": "preview/src/games/fire/styles.css",                          "purpose": "Location line below mission name"},
        {"name": "demand-label",           "name_type": "css_class",       "file_path": "preview/src/games/fire/styles.css",                          "purpose": "Small label above demand number"},
        {"name": "demand-value",           "name_type": "css_class",       "file_path": "preview/src/games/fire/styles.css",                          "purpose": "Large bold arithmetic target number"},
        {"name": "truck-yard",             "name_type": "css_class",       "file_path": "preview/src/games/fire/styles.css",                          "purpose": "Wrapping flex container for truck cards"},
        {"name": "truck-card",             "name_type": "css_class",       "file_path": "preview/src/games/fire/styles.css",                          "purpose": "Individual tappable truck unit"},
        {"name": "truck-selected",         "name_type": "css_class",       "file_path": "preview/src/games/fire/styles.css",                          "purpose": "Applied when truck is in dispatched array"},
        {"name": "truck-emoji",            "name_type": "css_class",       "file_path": "preview/src/games/fire/styles.css",                          "purpose": "Truck emoji display within card"},
        {"name": "truck-capacity",         "name_type": "css_class",       "file_path": "preview/src/games/fire/styles.css",                          "purpose": "Capacity label below truck emoji"},
        {"name": "dispatch-board",         "name_type": "css_class",       "file_path": "preview/src/games/fire/styles.css",                          "purpose": "Running total and dispatched truck display container"},
        {"name": "board-trucks",           "name_type": "css_class",       "file_path": "preview/src/games/fire/styles.css",                          "purpose": "Row of dispatched truck emojis"},
        {"name": "board-truck",            "name_type": "css_class",       "file_path": "preview/src/games/fire/styles.css",                          "purpose": "Single dispatched truck emoji"},
        {"name": "board-total",            "name_type": "css_class",       "file_path": "preview/src/games/fire/styles.css",                          "purpose": "Large running capacity total number"},
        {"name": "board-demand",           "name_type": "css_class",       "file_path": "preview/src/games/fire/styles.css",                          "purpose": "'of N needed' label below total"},
        {"name": "board-excess",           "name_type": "css_class",       "file_path": "preview/src/games/fire/styles.css",                          "purpose": "Applied to board-total when excess — turns red"},
        {"name": "timer-bar",              "name_type": "css_class",       "file_path": "preview/src/games/fire/styles.css",                          "purpose": "Track div for countdown timer fill"},
        {"name": "timer-fill",             "name_type": "css_class",       "file_path": "preview/src/games/fire/styles.css",                          "purpose": "Fill div, width driven by timePercent"},
        {"name": "timer-urgent",           "name_type": "css_class",       "file_path": "preview/src/games/fire/styles.css",                          "purpose": "Applied when timeLeft < 5 to trigger pulse animation"},
        {"name": "dispatch-hud",           "name_type": "css_class",       "file_path": "preview/src/games/fire/styles.css",                          "purpose": "Persistent HUD strip: score, lives, level"},
        {"name": "outcome-overlay",        "name_type": "css_class",       "file_path": "preview/src/games/fire/styles.css",                          "purpose": "Fixed inset-0 base overlay class"},
        {"name": "overlay-success",        "name_type": "css_class",       "file_path": "preview/src/games/fire/styles.css",                          "purpose": "Green background for successful dispatch"},
        {"name": "overlay-excess",         "name_type": "css_class",       "file_path": "preview/src/games/fire/styles.css",                          "purpose": "Red background for excess capacity"},
        {"name": "overlay-timeout",        "name_type": "css_class",       "file_path": "preview/src/games/fire/styles.css",                          "purpose": "Orange background for timeout"},
        {"name": "overlay-end",            "name_type": "css_class",       "file_path": "preview/src/games/fire/styles.css",                          "purpose": "Dark blue background for shift-end summary"},
        {"name": "overlay-inner",          "name_type": "css_class",       "file_path": "preview/src/games/fire/styles.css",                          "purpose": "Centered content wrapper inside overlay"},
        {"name": "overlay-emoji",          "name_type": "css_class",       "file_path": "preview/src/games/fire/styles.css",                          "purpose": "Large reaction emoji inside overlay"},
        {"name": "overlay-title",          "name_type": "css_class",       "file_path": "preview/src/games/fire/styles.css",                          "purpose": "Bold outcome title inside overlay"},
        {"name": "overlay-subtitle",       "name_type": "css_class",       "file_path": "preview/src/games/fire/styles.css",                          "purpose": "Secondary message inside overlay"},
        {"name": "truck-bounce",           "name_type": "keyframe",        "file_path": "preview/src/games/fire/styles.css",                          "purpose": "Snappy scale-up bounce when truck is selected"},
        {"name": "dispatch-shake",         "name_type": "keyframe",        "file_path": "preview/src/games/fire/styles.css",                          "purpose": "Horizontal rejection shake on excess dispatch"},
        {"name": "overlay-enter",          "name_type": "keyframe",        "file_path": "preview/src/games/fire/styles.css",                          "purpose": "Scale-in entry for outcome overlay"},
        {"name": "timer-pulse",            "name_type": "keyframe",        "file_path": "preview/src/games/fire/styles.css",                          "purpose": "Opacity pulse for urgent timer fill"},
    ],
    "animation_contracts": [
        {
            "animation_id": "truck-bounce",
            "trigger": "truck-selected class applied on truck toggle",
            "duration_ms": 300,
            "easing": "ease",
            "css_custom_properties": [],
            "keyframe_name": "truck-bounce",
            "owner_file": "preview/src/games/fire/styles.css",
            "element_selector": ".truck-card.truck-selected",
            "dom_measurement_required": False,
        },
        {
            "animation_id": "dispatch-shake",
            "trigger": "excess-shake class applied on totalCapacity > demandValue",
            "duration_ms": 350,
            "easing": "ease",
            "css_custom_properties": [],
            "keyframe_name": "dispatch-shake",
            "owner_file": "preview/src/games/fire/styles.css",
            "element_selector": ".dispatch-board",
            "dom_measurement_required": False,
        },
        {
            "animation_id": "overlay-enter",
            "trigger": "OutcomeOverlay renders (feedbackMode non-null)",
            "duration_ms": 200,
            "easing": "cubic-bezier(0.17, 0.89, 0.32, 1.1)",
            "css_custom_properties": [],
            "keyframe_name": "overlay-enter",
            "owner_file": "preview/src/games/fire/styles.css",
            "element_selector": ".outcome-overlay",
            "dom_measurement_required": False,
        },
        {
            "animation_id": "timer-pulse",
            "trigger": "timer-urgent class applied when timeLeft < 5",
            "duration_ms": 500,
            "easing": "ease",
            "css_custom_properties": [],
            "keyframe_name": "timer-pulse",
            "owner_file": "preview/src/games/fire/styles.css",
            "element_selector": ".timer-fill.timer-urgent",
            "dom_measurement_required": False,
        },
    ],
    "acceptance_signals": [
        {
            "signal_id": "AS1-01",
            "description": "Mission card shows incident with readable demand value",
            "observable_in_browser": "Large amber number indicates how much truck capacity is needed; incident emoji and location visible",
            "related_patches": ["P1-05", "P1-09"],
        },
        {
            "signal_id": "AS1-02",
            "description": "Tapping a truck selects it and updates running total",
            "observable_in_browser": "Truck card gets green border; dispatch board total increments by truck capacity",
            "related_patches": ["P1-06", "P1-07", "P1-09"],
        },
        {
            "signal_id": "AS1-03",
            "description": "Correct dispatch triggers success overlay",
            "observable_in_browser": "When totalCapacity === demandValue and dispatch is submitted, green overlay appears",
            "related_patches": ["P1-08", "P1-09"],
        },
        {
            "signal_id": "AS1-04",
            "description": "Excess triggers board shake and red total",
            "observable_in_browser": "When totalCapacity > demandValue, board shakes and total turns red",
            "related_patches": ["P1-04", "P1-07", "P1-09"],
        },
        {
            "signal_id": "AS1-05",
            "description": "Timer depletes and causes a timeout miss",
            "observable_in_browser": "Timer fill bar empties in real time; at zero, orange overlay appears and lives decrement",
            "related_patches": ["P1-03", "P1-09"],
        },
        {
            "signal_id": "AS1-06",
            "description": "Timer turns urgent at low time",
            "observable_in_browser": "Fill bar pulses when timeLeft < 5 — visible urgency signal without text",
            "related_patches": ["P1-03", "P1-04"],
        },
    ],
    "patch_notes": (
        "Pass 1 creates the full file structure from implementation_plan.file_plan. "
        "The dispatch mechanic is multi-select (multiple trucks), unlike Bakery's single-tap. "
        "totalCapacity is recomputed as a simple sum on every truck toggle — no separate addReducer needed. "
        "EXCESS feedback keeps the current dispatch visible so the player can correct it by deselecting a truck. "
        "This is distinct from Bakery's bounce-back, which removes the item automatically. "
        "Timer must pause (clearInterval) whenever feedbackMode is non-null, "
        "and restart fresh for the new incident when it loads."
    ),
}


# ---------------------------------------------------------------------------
# Unit Circle Pizza Lab — navigate_and_position interaction — Pass 1
# ---------------------------------------------------------------------------

_UNIT_CIRCLE_PATCH_PLAN: Dict[str, Any] = {
    "patch_objective": (
        "Create the initial playable Unit Circle Pizza Lab prototype: lab config data, "
        "five UI components (OrderPanel, PizzaWheel, AngleReadout, CoordinateDisplay, FeedbackPanel), "
        "styles, and the UnitCirclePrototype root container with angle evaluation and round loop logic."
    ),
    "source_pass": {
        "pass_number": 1,
        "pass_label": "Core Angle Placement Loop",
        "features_added": [
            "Lab config data: round configs with target angles, tolerances, and difficulty levels",
            "Common angles lookup table (0°, 30°, 45°, 60°, 90°, etc.) with exact trig values",
            "OrderPanel component: shows target angle specification for the current round",
            "PizzaWheel component: clickable SVG unit circle with topping placement marker",
            "AngleReadout component: live display of player's angle in degrees and radians",
            "CoordinateDisplay component: live (cos θ, sin θ) values computed from player's angle",
            "FeedbackPanel component: inline result with correctness, delta, and correct-answer reveal",
            "UnitCirclePrototype: root container with full round state, evaluation logic, and progression",
        ],
    },
    "target_files": [
        {
            "file_path": "preview/src/App.jsx",
            "operation": "edit",
            "current_state": "Mounts previous game component or placeholder",
            "post_patch_state": "Mounts UnitCirclePrototype as the active game component",
        },
        {
            "file_path": "preview/src/games/UnitCirclePrototype.jsx",
            "operation": "create",
            "current_state": "File does not exist",
            "post_patch_state": "Root container with full round state, angle evaluation, and session progression",
        },
        {
            "file_path": "preview/src/games/unitcircle/labConfig.js",
            "operation": "create",
            "current_state": "File does not exist",
            "post_patch_state": "Exports ROUND_CONFIGS array and COMMON_ANGLES lookup table",
        },
        {
            "file_path": "preview/src/games/unitcircle/components/OrderPanel.jsx",
            "operation": "create",
            "current_state": "File does not exist",
            "post_patch_state": "Presentational component showing the target angle specification for the current round",
        },
        {
            "file_path": "preview/src/games/unitcircle/components/PizzaWheel.jsx",
            "operation": "create",
            "current_state": "File does not exist",
            "post_patch_state": "SVG unit circle with clickable surface, player topping marker, and optional correct-position ghost",
        },
        {
            "file_path": "preview/src/games/unitcircle/components/AngleReadout.jsx",
            "operation": "create",
            "current_state": "File does not exist",
            "post_patch_state": "Live display of current angle in degrees and radians",
        },
        {
            "file_path": "preview/src/games/unitcircle/components/CoordinateDisplay.jsx",
            "operation": "create",
            "current_state": "File does not exist",
            "post_patch_state": "Live (cos θ, sin θ) values computed from current angle, updating on every change",
        },
        {
            "file_path": "preview/src/games/unitcircle/components/FeedbackPanel.jsx",
            "operation": "create",
            "current_state": "File does not exist",
            "post_patch_state": "Inline result panel showing correct/close/miss verdict, delta, and correct answer reveal",
        },
        {
            "file_path": "preview/src/games/unitcircle/styles.css",
            "operation": "create",
            "current_state": "File does not exist",
            "post_patch_state": "All layout, SVG, and animation styles scoped to .pizza-lab class",
        },
    ],
    "patch_sequence": [
        {
            "patch_id": "P1-01",
            "file_path": "preview/src/games/unitcircle/labConfig.js",
            "patch_type": "add_constant",
            "change_description": (
                "Export ROUND_CONFIGS as the default export — array of round objects grouped into 3 difficulty tiers. "
                "Tier 1 (rounds 1–5): quadrant angles (0°, 90°, 180°, 270°) with toleranceDeg 15. "
                "Tier 2 (rounds 6–10): common angles (30°, 45°, 60°, 120°, 135°, 150°, 210°, 225°, 240°) with toleranceDeg 10. "
                "Tier 3 (rounds 11–15): all standard angles including 315°, 300°, 330° with toleranceDeg 5. "
                "Each round object: {targetAngleDeg, toleranceDeg, label (e.g. '30°'), "
                "specType ('angle'|'coords'|'radians'), displaySpec (the string shown to player)}."
            ),
            "location_hint": "Top of file, default export",
            "named_elements": ["constant:ROUND_CONFIGS"],
            "depends_on": [],
            "rationale": "Round config is the authoritative source for difficulty progression and target angles.",
        },
        {
            "patch_id": "P1-02",
            "file_path": "preview/src/games/unitcircle/labConfig.js",
            "patch_type": "add_constant",
            "change_description": (
                "Export COMMON_ANGLES as a named const object mapping angle in degrees to exact trig values. "
                "Keys: 0, 30, 45, 60, 90, 120, 135, 150, 180, 210, 225, 240, 270, 300, 315, 330, 360. "
                "Each value: {cos: exact fraction string, sin: exact fraction string, "
                "rad: radian string (e.g. 'π/6'), cosDecimal: number, sinDecimal: number}. "
                "Example: 30 → {cos: '√3/2', sin: '1/2', rad: 'π/6', cosDecimal: 0.866, sinDecimal: 0.5}. "
                "Used by CoordinateDisplay and FeedbackPanel to show exact values for common angles."
            ),
            "location_hint": "After ROUND_CONFIGS default export",
            "named_elements": ["constant:COMMON_ANGLES"],
            "depends_on": ["P1-01"],
            "rationale": "Exact trig values at common angles must be looked up, not computed — floating point shows non-exact representations.",
        },
        {
            "patch_id": "P1-03",
            "file_path": "preview/src/games/unitcircle/styles.css",
            "patch_type": "add_css_class",
            "change_description": (
                "Create the full stylesheet for the Pizza Lab. "
                "Root: .pizza-lab (flex column, 100vh, background #fdf6ec, font-family sans-serif, overflow hidden). "
                "Wheel container: .pizza-wheel-container (display flex, justify-content center, position relative). "
                ".unit-circle-svg (cursor crosshair, max-width 340px, width 100%). "
                "SVG elements (referenced via className on SVG child elements): "
                ".circle-outline (fill none, stroke #d1d5db, stroke-width 2). "
                ".axis-line (stroke #9ca3af, stroke-width 1, stroke-dasharray 4 4). "
                ".player-topping (fill #f97316, stroke #fff, stroke-width 2, "
                "animation topping-pop 0.25s cubic-bezier(0.17,0.89,0.32,1.4) forwards when first placed). "
                ".correct-ghost (fill none, stroke #22c55e, stroke-width 2, stroke-dasharray 5 3, opacity 0.8). "
                "Angle readout: .angle-readout (display flex, gap 16px, justify-content center, font-size 1.1rem). "
                ".angle-deg (font-weight 700, font-size 1.4rem). "
                ".angle-rad (color #6b7280, font-size 1rem). "
                "Coordinate display: .coord-display (display flex, gap 24px, justify-content center). "
                ".coord-label (font-size 0.75rem, uppercase, letter-spacing 0.06em, color #9ca3af). "
                ".coord-value (font-size 1.3rem, font-weight 700). "
                ".coord-exact (font-size 0.8rem, color #6b7280). "
                "Order panel: .order-panel (background #fff, border 2px solid #e5e7eb, border-radius 12px, padding 16px). "
                ".order-label (font-size 0.75rem, uppercase, letter-spacing 0.08em, color #9ca3af). "
                ".order-spec (font-size 2rem, font-weight 800). "
                "Submit button: .submit-btn (background #6366f1, color #fff, border none, border-radius 999px, "
                "padding 12px 32px, font-size 1rem, font-weight 700, cursor pointer, transition 0.15s). "
                ".submit-btn:disabled (opacity 0.4, cursor not-allowed). "
                "Feedback panel: .feedback-panel (border-radius 12px, padding 16px, text-align center). "
                ".feedback-correct (background #dcfce7, border 2px solid #22c55e). "
                ".feedback-close (background #fef3c7, border 2px solid #f59e0b). "
                ".feedback-miss (background #fee2e2, border 2px solid #ef4444). "
                ".feedback-verdict (font-size 1.2rem, font-weight 700). "
                ".feedback-delta (font-size 0.9rem, color #6b7280, margin-top 4px). "
                ".feedback-answer (font-size 0.85rem, margin-top 8px, color #374151). "
                "Session HUD: .session-hud (display flex, align-items center, gap 16px, padding 12px 16px). "
                ".round-counter (font-size 0.9rem, color #6b7280). "
                ".session-score (font-size 1rem, font-weight 700)."
            ),
            "location_hint": "Full file content — new file",
            "named_elements": [
                "css_class:pizza-lab",
                "css_class:pizza-wheel-container", "css_class:unit-circle-svg",
                "css_class:circle-outline", "css_class:axis-line",
                "css_class:player-topping", "css_class:correct-ghost",
                "css_class:angle-readout", "css_class:angle-deg", "css_class:angle-rad",
                "css_class:coord-display", "css_class:coord-label",
                "css_class:coord-value", "css_class:coord-exact",
                "css_class:order-panel", "css_class:order-label", "css_class:order-spec",
                "css_class:submit-btn",
                "css_class:feedback-panel", "css_class:feedback-correct",
                "css_class:feedback-close", "css_class:feedback-miss",
                "css_class:feedback-verdict", "css_class:feedback-delta", "css_class:feedback-answer",
                "css_class:session-hud", "css_class:round-counter", "css_class:session-score",
            ],
            "depends_on": [],
            "rationale": "All layout primitives and SVG class styles must exist before PizzaWheel renders SVG content.",
        },
        {
            "patch_id": "P1-04",
            "file_path": "preview/src/games/unitcircle/styles.css",
            "patch_type": "add_keyframe",
            "change_description": (
                "Add three keyframes. "
                "topping-pop: from scale(0.3) opacity(0) to scale(1) opacity(1) with cubic-bezier(0.17,0.89,0.32,1.4) — "
                "snappy pop when the player topping is first placed after submit. "
                "correct-flash: 0%/100% background-color transparent, 50% background-color rgba(34,197,94,0.2) — "
                "brief green flash on the entire feedback-panel when answer is correct. "
                "miss-arc: 0% stroke-dashoffset 100, 100% stroke-dashoffset 0 — "
                "arc draw animation for the correct-ghost marker revealing the correct position."
            ),
            "location_hint": "After all CSS class rules, end of file",
            "named_elements": ["keyframe:topping-pop", "keyframe:correct-flash", "keyframe:miss-arc"],
            "depends_on": ["P1-03"],
            "rationale": "Keyframes must be in the same file as the classes that reference them.",
        },
        {
            "patch_id": "P1-05",
            "file_path": "preview/src/games/unitcircle/components/OrderPanel.jsx",
            "patch_type": "add_component",
            "change_description": (
                "Create OrderPanel as a default export function. "
                "Props: targetSpec (string — the text shown to the player, e.g. '45°' or 'cos 60°, sin 60°' or 'π/4'). "
                "Render: outer div class order-panel. "
                "order-label div ('Place your topping at:'). "
                "order-spec div (targetSpec rendered as a large, bold display). "
                "If targetSpec contains 'cos' or 'sin', render as two lines for readability."
            ),
            "location_hint": "Full file content — new file",
            "named_elements": [
                "component:OrderPanel",
                "prop:targetSpec",
            ],
            "depends_on": ["P1-03"],
            "rationale": "OrderPanel is purely presentational — it receives the pre-formatted spec string from the root container.",
        },
        {
            "patch_id": "P1-06",
            "file_path": "preview/src/games/unitcircle/components/PizzaWheel.jsx",
            "patch_type": "add_component",
            "change_description": (
                "Create PizzaWheel as a default export function. "
                "Props: currentAngleDeg (number 0–360), toppingPlaced (boolean), "
                "correctAngleDeg (number|null), showCorrectPosition (boolean), "
                "onAngleChange (function(angleDeg: number) => void). "
                "Render: div class pizza-wheel-container containing an SVG element class unit-circle-svg, "
                "viewBox '-1.3 -1.3 2.6 2.6', preserveAspectRatio xMidYMid meet. "
                "SVG contents: "
                "(1) circle class circle-outline cx=0 cy=0 r=1 — the unit circle. "
                "(2) Two axis lines (horizontal and vertical) class axis-line. "
                "(3) Player topping: when toppingPlaced is true, render a circle class player-topping "
                "at cx=cos(currentAngleDeg * π/180) cy=-sin(currentAngleDeg * π/180) r=0.08. "
                "(Note: SVG y-axis is inverted, so use -sin to place correctly.) "
                "(4) Correct ghost: when showCorrectPosition is true and correctAngleDeg is non-null, "
                "render a circle class correct-ghost at cx=cos(correctAngleDeg * π/180) cy=-sin(correctAngleDeg * π/180) r=0.1. "
                "Click handler on the SVG: convert click coordinates to unit circle angle using "
                "Math.atan2(-dy, dx) * 180/π (adjusting for inverted y), normalize to 0–360, call onAngleChange."
            ),
            "location_hint": "Full file content — new file",
            "named_elements": [
                "component:PizzaWheel",
                "prop:currentAngleDeg", "prop:toppingPlaced", "prop:correctAngleDeg",
                "prop:showCorrectPosition", "prop:onAngleChange",
            ],
            "depends_on": ["P1-03"],
            "rationale": "PizzaWheel owns the SVG coordinate mapping and angle input — all math is in the click handler, not the root container.",
        },
        {
            "patch_id": "P1-07",
            "file_path": "preview/src/games/unitcircle/components/AngleReadout.jsx",
            "patch_type": "add_component",
            "change_description": (
                "Create AngleReadout as a default export function. "
                "Props: angleDeg (number). "
                "Render: div class angle-readout. "
                "angle-deg span: Math.round(angleDeg) + '°'. "
                "angle-rad span: compute radian value = (angleDeg * π/180).toFixed(3) + ' rad'. "
                "If angleDeg matches a COMMON_ANGLES key within 0.5°, show the exact radian string "
                "(e.g. 'π/6') instead of the decimal."
            ),
            "location_hint": "Full file content — new file",
            "named_elements": [
                "component:AngleReadout",
                "prop:angleDeg",
            ],
            "depends_on": ["P1-03"],
            "rationale": "AngleReadout gives immediate feedback as the player explores the wheel — it updates live on every click.",
        },
        {
            "patch_id": "P1-08",
            "file_path": "preview/src/games/unitcircle/components/CoordinateDisplay.jsx",
            "patch_type": "add_component",
            "change_description": (
                "Create CoordinateDisplay as a default export function. "
                "Props: angleDeg (number). "
                "Compute cosVal = Math.cos(angleDeg * π/180), sinVal = Math.sin(angleDeg * π/180). "
                "Render: div class coord-display. "
                "Two blocks side by side: "
                "Block 1: coord-label div ('cos θ'), coord-value div (cosVal.toFixed(3)), "
                "coord-exact div showing exact fraction from COMMON_ANGLES if angleDeg is a common angle. "
                "Block 2: coord-label div ('sin θ'), coord-value div (sinVal.toFixed(3)), "
                "coord-exact div showing exact fraction from COMMON_ANGLES if applicable."
            ),
            "location_hint": "Full file content — new file",
            "named_elements": [
                "component:CoordinateDisplay",
                "prop:angleDeg",
            ],
            "depends_on": ["P1-03"],
            "rationale": "CoordinateDisplay teaches the (cos θ, sin θ) mapping by showing live values as the player moves — the learning is in the motion.",
        },
        {
            "patch_id": "P1-09",
            "file_path": "preview/src/games/unitcircle/components/FeedbackPanel.jsx",
            "patch_type": "add_component",
            "change_description": (
                "Create FeedbackPanel as a default export function. "
                "Props: feedbackMode (string|null: 'correct'|'close'|'miss'|null), "
                "deltaAngle (number — absolute difference from target), "
                "correctAngleDeg (number), playerAngleDeg (number). "
                "Returns null when feedbackMode is null. "
                "Render: div class feedback-panel plus feedback-correct/feedback-close/feedback-miss variant. "
                "feedback-verdict div: 'Perfect!' (correct) / 'Close!' (close) / 'Not quite.' (miss). "
                "feedback-delta div: 'You were ' + deltaAngle.toFixed(1) + '° off'. Hidden when correct. "
                "feedback-answer div (visible on close and miss): "
                "'Correct position: ' + correctAngleDeg + '° → (' + cosStr + ', ' + sinStr + ')' "
                "using COMMON_ANGLES lookup or decimal fallback."
            ),
            "location_hint": "Full file content — new file",
            "named_elements": [
                "component:FeedbackPanel",
                "prop:feedbackMode", "prop:deltaAngle", "prop:correctAngleDeg", "prop:playerAngleDeg",
            ],
            "depends_on": ["P1-03"],
            "rationale": "FeedbackPanel teaches on miss — showing the exact correct position with coordinates is the primary learning moment.",
        },
        {
            "patch_id": "P1-10",
            "file_path": "preview/src/games/UnitCirclePrototype.jsx",
            "patch_type": "add_component",
            "change_description": (
                "Create UnitCirclePrototype as a default export function. "
                "Imports: ROUND_CONFIGS, COMMON_ANGLES from './unitcircle/labConfig'. "
                "Imports: OrderPanel, PizzaWheel, AngleReadout, CoordinateDisplay, FeedbackPanel from './unitcircle/components/'. "
                "Imports: './unitcircle/styles.css'. "
                "Module constants: ROUNDS_PER_SESSION = ROUND_CONFIGS.length, "
                "ADVANCE_MS = 1800 (time before advancing after feedback). "
                "State: roundIndex (0), currentAngleDeg (0), toppingPlaced (false), "
                "submitted (false), feedbackMode (null), score (0), streak (0), sessionComplete (false). "
                "Derived: currentRound = ROUND_CONFIGS[roundIndex], "
                "targetAngleDeg = currentRound.targetAngleDeg, "
                "toleranceDeg = currentRound.toleranceDeg, "
                "deltaAngle = Math.abs(currentAngleDeg - targetAngleDeg) normalized to 0–180 "
                "(use min(delta, 360 - delta) to handle wrap-around). "
                "showCorrectPosition = submitted and feedbackMode !== 'correct'. "
                "handleAngleChange(deg): set currentAngleDeg = deg, set toppingPlaced = true "
                "(only before submit — ignore if submitted). "
                "handleSubmit(): if not toppingPlaced or submitted, return. "
                "Set submitted = true. "
                "If deltaAngle <= toleranceDeg: set feedbackMode 'correct', increment score, increment streak. "
                "Else if deltaAngle <= toleranceDeg * 2.5: set feedbackMode 'close', reset streak. "
                "Else: set feedbackMode 'miss', reset streak. "
                "After ADVANCE_MS: if roundIndex < ROUNDS_PER_SESSION - 1: increment roundIndex, reset round state. "
                "Else: set sessionComplete true. "
                "Render: root div class pizza-lab. "
                "session-hud: round-counter ('Round ' + (roundIndex+1) + '/' + ROUNDS_PER_SESSION), "
                "session-score (score). "
                "OrderPanel (targetSpec = currentRound.displaySpec). "
                "PizzaWheel (currentAngleDeg, toppingPlaced, correctAngleDeg = targetAngleDeg if showCorrectPosition, "
                "showCorrectPosition, onAngleChange = handleAngleChange). "
                "AngleReadout (angleDeg = currentAngleDeg). "
                "CoordinateDisplay (angleDeg = currentAngleDeg). "
                "Submit button class submit-btn, disabled when submitted or not toppingPlaced, onClick = handleSubmit. "
                "FeedbackPanel (feedbackMode, deltaAngle, correctAngleDeg = targetAngleDeg, playerAngleDeg = currentAngleDeg)."
            ),
            "location_hint": "Full file content — new file",
            "named_elements": [
                "component:UnitCirclePrototype",
                "state_variable:roundIndex", "state_variable:currentAngleDeg",
                "state_variable:toppingPlaced", "state_variable:submitted",
                "state_variable:feedbackMode", "state_variable:score",
                "state_variable:streak", "state_variable:sessionComplete",
                "constant:ROUNDS_PER_SESSION", "constant:ADVANCE_MS",
                "callback:handleAngleChange", "callback:handleSubmit",
            ],
            "depends_on": ["P1-01", "P1-02", "P1-03", "P1-04", "P1-05", "P1-06", "P1-07", "P1-08", "P1-09"],
            "rationale": "Root container must be built last — it owns all state and depends on every child component and the lab config.",
        },
        {
            "patch_id": "P1-11",
            "file_path": "preview/src/App.jsx",
            "patch_type": "edit_render_output",
            "change_description": (
                "Add import for UnitCirclePrototype: import UnitCirclePrototype from './games/UnitCirclePrototype'. "
                "Replace the current active game component in App's return statement with <UnitCirclePrototype />. "
                "Remove import for any previous game component no longer referenced."
            ),
            "location_hint": "Import block at top of file and App function return statement",
            "named_elements": ["component:UnitCirclePrototype"],
            "depends_on": ["P1-10"],
            "rationale": "App.jsx is the preview entry mount. UnitCirclePrototype must be mounted here for the preview to render.",
        },
    ],
    "naming_registry": [
        {"name": "ROUND_CONFIGS",          "name_type": "constant",        "file_path": "preview/src/games/unitcircle/labConfig.js",                      "purpose": "Array of round configs with targetAngleDeg, toleranceDeg, and displaySpec"},
        {"name": "COMMON_ANGLES",          "name_type": "constant",        "file_path": "preview/src/games/unitcircle/labConfig.js",                      "purpose": "Lookup table of exact trig values at standard angles"},
        {"name": "ROUNDS_PER_SESSION",     "name_type": "constant",        "file_path": "preview/src/games/UnitCirclePrototype.jsx",                      "purpose": "Total rounds in one session, derived from ROUND_CONFIGS.length"},
        {"name": "ADVANCE_MS",             "name_type": "constant",        "file_path": "preview/src/games/UnitCirclePrototype.jsx",                      "purpose": "Duration in ms after feedback before advancing to next round"},
        {"name": "UnitCirclePrototype",    "name_type": "component",       "file_path": "preview/src/games/UnitCirclePrototype.jsx",                      "purpose": "Root container — owns all round state, angle evaluation, and session progression"},
        {"name": "OrderPanel",             "name_type": "component",       "file_path": "preview/src/games/unitcircle/components/OrderPanel.jsx",         "purpose": "Shows the target angle specification for the current round"},
        {"name": "PizzaWheel",             "name_type": "component",       "file_path": "preview/src/games/unitcircle/components/PizzaWheel.jsx",         "purpose": "Clickable SVG unit circle that emits angle changes"},
        {"name": "AngleReadout",           "name_type": "component",       "file_path": "preview/src/games/unitcircle/components/AngleReadout.jsx",       "purpose": "Live display of current angle in degrees and radians"},
        {"name": "CoordinateDisplay",      "name_type": "component",       "file_path": "preview/src/games/unitcircle/components/CoordinateDisplay.jsx",  "purpose": "Live (cos θ, sin θ) values computed from current angle"},
        {"name": "FeedbackPanel",          "name_type": "component",       "file_path": "preview/src/games/unitcircle/components/FeedbackPanel.jsx",      "purpose": "Inline result with verdict, delta, and correct-answer reveal"},
        {"name": "roundIndex",             "name_type": "state_variable",  "file_path": "preview/src/games/UnitCirclePrototype.jsx",                      "purpose": "0-based index into ROUND_CONFIGS"},
        {"name": "currentAngleDeg",        "name_type": "state_variable",  "file_path": "preview/src/games/UnitCirclePrototype.jsx",                      "purpose": "Player's currently selected angle in degrees (0–360)"},
        {"name": "toppingPlaced",          "name_type": "state_variable",  "file_path": "preview/src/games/UnitCirclePrototype.jsx",                      "purpose": "True after the player clicks the wheel for the first time in a round"},
        {"name": "submitted",              "name_type": "state_variable",  "file_path": "preview/src/games/UnitCirclePrototype.jsx",                      "purpose": "True after the player confirms their angle with the submit button"},
        {"name": "feedbackMode",           "name_type": "state_variable",  "file_path": "preview/src/games/UnitCirclePrototype.jsx",                      "purpose": "Result of evaluation: correct, close, miss, or null"},
        {"name": "score",                  "name_type": "state_variable",  "file_path": "preview/src/games/UnitCirclePrototype.jsx",                      "purpose": "Session score — increments only on correct answers"},
        {"name": "streak",                 "name_type": "state_variable",  "file_path": "preview/src/games/UnitCirclePrototype.jsx",                      "purpose": "Consecutive correct answers — resets on close or miss"},
        {"name": "sessionComplete",        "name_type": "state_variable",  "file_path": "preview/src/games/UnitCirclePrototype.jsx",                      "purpose": "True when all rounds are complete"},
        {"name": "handleAngleChange",      "name_type": "callback",        "file_path": "preview/src/games/UnitCirclePrototype.jsx",                      "purpose": "Receives angle from PizzaWheel click and updates currentAngleDeg"},
        {"name": "handleSubmit",           "name_type": "callback",        "file_path": "preview/src/games/UnitCirclePrototype.jsx",                      "purpose": "Evaluates currentAngleDeg against target and sets feedbackMode"},
        {"name": "targetSpec",             "name_type": "prop",            "file_path": "preview/src/games/unitcircle/components/OrderPanel.jsx",         "purpose": "Pre-formatted spec string shown to the player (angle, coords, or radians)"},
        {"name": "toppingPlaced",          "name_type": "prop",            "file_path": "preview/src/games/unitcircle/components/PizzaWheel.jsx",         "purpose": "Controls whether the player topping SVG element is rendered"},
        {"name": "correctAngleDeg",        "name_type": "prop",            "file_path": "preview/src/games/unitcircle/components/PizzaWheel.jsx",         "purpose": "Angle of the correct-ghost marker, passed when showCorrectPosition is true"},
        {"name": "showCorrectPosition",    "name_type": "prop",            "file_path": "preview/src/games/unitcircle/components/PizzaWheel.jsx",         "purpose": "When true, renders the correct-ghost marker at correctAngleDeg"},
        {"name": "onAngleChange",          "name_type": "prop",            "file_path": "preview/src/games/unitcircle/components/PizzaWheel.jsx",         "purpose": "Callback invoked with the computed angle when the user clicks the SVG"},
        {"name": "angleDeg",               "name_type": "prop",            "file_path": "preview/src/games/unitcircle/components/AngleReadout.jsx",       "purpose": "Current angle in degrees to display"},
        {"name": "deltaAngle",             "name_type": "prop",            "file_path": "preview/src/games/unitcircle/components/FeedbackPanel.jsx",      "purpose": "Absolute angular difference between player and target — shown on close and miss"},
        {"name": "playerAngleDeg",         "name_type": "prop",            "file_path": "preview/src/games/unitcircle/components/FeedbackPanel.jsx",      "purpose": "Player's submitted angle, used in comparison display"},
        {"name": "pizza-lab",              "name_type": "css_class",       "file_path": "preview/src/games/unitcircle/styles.css",                        "purpose": "Root game wrapper: light background flex column"},
        {"name": "pizza-wheel-container",  "name_type": "css_class",       "file_path": "preview/src/games/unitcircle/styles.css",                        "purpose": "Centering wrapper for the SVG unit circle"},
        {"name": "unit-circle-svg",        "name_type": "css_class",       "file_path": "preview/src/games/unitcircle/styles.css",                        "purpose": "The SVG element: crosshair cursor, max-width 340px"},
        {"name": "circle-outline",         "name_type": "css_class",       "file_path": "preview/src/games/unitcircle/styles.css",                        "purpose": "The unit circle ring stroke — no fill"},
        {"name": "axis-line",              "name_type": "css_class",       "file_path": "preview/src/games/unitcircle/styles.css",                        "purpose": "Horizontal and vertical dashed axis lines"},
        {"name": "player-topping",         "name_type": "css_class",       "file_path": "preview/src/games/unitcircle/styles.css",                        "purpose": "Orange filled circle marking the player's selected position"},
        {"name": "correct-ghost",          "name_type": "css_class",       "file_path": "preview/src/games/unitcircle/styles.css",                        "purpose": "Dashed green circle marking the correct position after miss"},
        {"name": "angle-readout",          "name_type": "css_class",       "file_path": "preview/src/games/unitcircle/styles.css",                        "purpose": "Row showing degrees and radians side by side"},
        {"name": "angle-deg",              "name_type": "css_class",       "file_path": "preview/src/games/unitcircle/styles.css",                        "purpose": "Large bold degree value"},
        {"name": "angle-rad",              "name_type": "css_class",       "file_path": "preview/src/games/unitcircle/styles.css",                        "purpose": "Smaller radian value beside degrees"},
        {"name": "coord-display",          "name_type": "css_class",       "file_path": "preview/src/games/unitcircle/styles.css",                        "purpose": "Row showing cos and sin values side by side"},
        {"name": "coord-label",            "name_type": "css_class",       "file_path": "preview/src/games/unitcircle/styles.css",                        "purpose": "Small uppercase label above coordinate value"},
        {"name": "coord-value",            "name_type": "css_class",       "file_path": "preview/src/games/unitcircle/styles.css",                        "purpose": "Bold decimal value for cos or sin"},
        {"name": "coord-exact",            "name_type": "css_class",       "file_path": "preview/src/games/unitcircle/styles.css",                        "purpose": "Exact fraction display below decimal (shown at common angles)"},
        {"name": "order-panel",            "name_type": "css_class",       "file_path": "preview/src/games/unitcircle/styles.css",                        "purpose": "Card container for the target specification"},
        {"name": "order-label",            "name_type": "css_class",       "file_path": "preview/src/games/unitcircle/styles.css",                        "purpose": "Small prompt text above the spec"},
        {"name": "order-spec",             "name_type": "css_class",       "file_path": "preview/src/games/unitcircle/styles.css",                        "purpose": "Large bold target specification display"},
        {"name": "submit-btn",             "name_type": "css_class",       "file_path": "preview/src/games/unitcircle/styles.css",                        "purpose": "Confirm button; disabled before topping is placed and after submit"},
        {"name": "feedback-panel",         "name_type": "css_class",       "file_path": "preview/src/games/unitcircle/styles.css",                        "purpose": "Inline result card base class"},
        {"name": "feedback-correct",       "name_type": "css_class",       "file_path": "preview/src/games/unitcircle/styles.css",                        "purpose": "Green border and background for correct answer"},
        {"name": "feedback-close",         "name_type": "css_class",       "file_path": "preview/src/games/unitcircle/styles.css",                        "purpose": "Amber border and background for near-miss"},
        {"name": "feedback-miss",          "name_type": "css_class",       "file_path": "preview/src/games/unitcircle/styles.css",                        "purpose": "Red border and background for incorrect answer"},
        {"name": "feedback-verdict",       "name_type": "css_class",       "file_path": "preview/src/games/unitcircle/styles.css",                        "purpose": "Bold verdict text (Perfect!/Close!/Not quite.)"},
        {"name": "feedback-delta",         "name_type": "css_class",       "file_path": "preview/src/games/unitcircle/styles.css",                        "purpose": "Angular offset displayed on close and miss"},
        {"name": "feedback-answer",        "name_type": "css_class",       "file_path": "preview/src/games/unitcircle/styles.css",                        "purpose": "Correct position reveal with coordinates on miss and close"},
        {"name": "session-hud",            "name_type": "css_class",       "file_path": "preview/src/games/unitcircle/styles.css",                        "purpose": "Persistent session status bar"},
        {"name": "round-counter",          "name_type": "css_class",       "file_path": "preview/src/games/unitcircle/styles.css",                        "purpose": "Round N of M display"},
        {"name": "session-score",          "name_type": "css_class",       "file_path": "preview/src/games/unitcircle/styles.css",                        "purpose": "Running session score in HUD"},
        {"name": "topping-pop",            "name_type": "keyframe",        "file_path": "preview/src/games/unitcircle/styles.css",                        "purpose": "Scale-in pop when player topping is placed on submit"},
        {"name": "correct-flash",          "name_type": "keyframe",        "file_path": "preview/src/games/unitcircle/styles.css",                        "purpose": "Brief green flash on feedback panel for correct answers"},
        {"name": "miss-arc",               "name_type": "keyframe",        "file_path": "preview/src/games/unitcircle/styles.css",                        "purpose": "Stroke draw animation for the correct-ghost reveal arc"},
        # Props with shared names — registry entry for PizzaWheel's currentAngleDeg and CoordinateDisplay's angleDeg
        {"name": "currentAngleDeg",        "name_type": "prop",            "file_path": "preview/src/games/unitcircle/components/PizzaWheel.jsx",         "purpose": "Player's current angle — used to position the player topping on the wheel"},
        {"name": "feedbackMode",           "name_type": "prop",            "file_path": "preview/src/games/unitcircle/components/FeedbackPanel.jsx",      "purpose": "Drives variant class and conditional rendering of delta and answer"},
    ],
    "animation_contracts": [
        {
            "animation_id": "topping-pop",
            "trigger": "toppingPlaced becomes true after handleSubmit is called",
            "duration_ms": 250,
            "easing": "cubic-bezier(0.17, 0.89, 0.32, 1.4)",
            "css_custom_properties": [],
            "keyframe_name": "topping-pop",
            "owner_file": "preview/src/games/unitcircle/styles.css",
            "element_selector": ".player-topping",
            "dom_measurement_required": False,
        },
        {
            "animation_id": "correct-flash",
            "trigger": "feedback-correct class applied on correct answer",
            "duration_ms": 400,
            "easing": "ease",
            "css_custom_properties": [],
            "keyframe_name": "correct-flash",
            "owner_file": "preview/src/games/unitcircle/styles.css",
            "element_selector": ".feedback-panel.feedback-correct",
            "dom_measurement_required": False,
        },
        {
            "animation_id": "miss-arc",
            "trigger": "correct-ghost renders when showCorrectPosition is true",
            "duration_ms": 500,
            "easing": "ease",
            "css_custom_properties": [],
            "keyframe_name": "miss-arc",
            "owner_file": "preview/src/games/unitcircle/styles.css",
            "element_selector": ".correct-ghost",
            "dom_measurement_required": False,
        },
    ],
    "acceptance_signals": [
        {
            "signal_id": "AS1-01",
            "description": "Clicking the pizza wheel moves the topping marker",
            "observable_in_browser": "Orange dot appears at the clicked position on the unit circle; angle readout updates live",
            "related_patches": ["P1-06", "P1-07", "P1-10"],
        },
        {
            "signal_id": "AS1-02",
            "description": "cos θ and sin θ values update as player explores the wheel",
            "observable_in_browser": "Decimal values in CoordinateDisplay change as player clicks different positions",
            "related_patches": ["P1-08", "P1-10"],
        },
        {
            "signal_id": "AS1-03",
            "description": "Correct answer shows green feedback",
            "observable_in_browser": "When submitted angle is within tolerance, feedback panel turns green with 'Perfect!'",
            "related_patches": ["P1-09", "P1-10"],
        },
        {
            "signal_id": "AS1-04",
            "description": "Miss reveals correct position on the wheel",
            "observable_in_browser": "When angle is outside tolerance, dashed green ghost appears at the correct position with coordinate reveal",
            "related_patches": ["P1-03", "P1-04", "P1-06", "P1-09", "P1-10"],
        },
        {
            "signal_id": "AS1-05",
            "description": "Exact fraction values shown at common angles",
            "observable_in_browser": "At 30°, CoordinateDisplay shows '√3/2' and '1/2' instead of only decimals",
            "related_patches": ["P1-02", "P1-08"],
        },
        {
            "signal_id": "AS1-06",
            "description": "Round counter advances after feedback",
            "observable_in_browser": "'Round 2/15' appears in HUD after first round completes",
            "related_patches": ["P1-10"],
        },
    ],
    "patch_notes": (
        "Pass 1 creates the full file structure from implementation_plan.file_plan. "
        "The unit circle interaction is fundamentally different from Bakery and Fire Dispatch: "
        "there is no running total — the player positions once per round, then confirms. "
        "The close/miss threshold uses toleranceDeg * 2.5 as a grace zone so the game teaches "
        "without being punishing at the start. "
        "SVG y-axis inversion (using -sin instead of sin) is critical — must not be omitted. "
        "COMMON_ANGLES lookup for exact values is the key teaching mechanism for this game. "
        "showCorrectPosition should only be true after submit, never during active positioning. "
        "ADVANCE_MS should be long enough to read the feedback (1800ms) but short enough not to break the session rhythm."
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
    "bakery":     _BAKERY_PATCH_PLAN,
    "fire":       _FIRE_DISPATCH_PATCH_PLAN,
    "unitcircle": _UNIT_CIRCLE_PATCH_PLAN,
}

# ---------------------------------------------------------------------------
# Stub callable
# ---------------------------------------------------------------------------


def implementation_patch_plan_stub(context: Dict[str, Any]) -> Dict[str, Any]:
    # Read world_theme from implementation_plan (available in allowed_reads).
    artifact_inputs = context.get("artifact_inputs", {})
    impl_plan = artifact_inputs.get("implementation_plan", {})
    world_theme = (
        impl_plan.get("implementation_goal", "")
        + " "
        + " ".join(
            f.get("path", "") for f in impl_plan.get("file_plan", [])
        )
    )

    concept_key = None
    for key in CONCEPT_OVERRIDES:
        if key in world_theme.lower():
            concept_key = key
            break

    plan = CONCEPT_OVERRIDES[concept_key] if concept_key else _GENERIC_PATCH_PLAN

    # Derive target_files from implementation_plan.file_plan when available,
    # mapping action (create/update) to operation (create/edit).
    _ACTION_TO_OP = {"create": "create", "update": "edit", "delete": "do_not_touch"}
    impl_file_plan = impl_plan.get("file_plan", [])
    if impl_file_plan:
        # Build a lookup from path → target_file entry from the plan constant
        plan_tf_by_path = {tf["file_path"]: tf for tf in plan.get("target_files", [])}
        derived_target_files = []
        for fp in impl_file_plan:
            path = fp.get("path", "")
            action = fp.get("action", "create")
            op = _ACTION_TO_OP.get(action, "create")
            if path in plan_tf_by_path:
                derived_target_files.append(plan_tf_by_path[path])
            else:
                derived_target_files.append({
                    "file_path": path,
                    "operation": op,
                    "current_state": "State not yet described for this file",
                    "post_patch_state": fp.get("purpose", "File created per implementation plan"),
                })
        target_files = derived_target_files
    else:
        target_files = plan["target_files"]

    # Record implementation_plan file paths for gate coverage validation.
    implementation_plan_files = [fp.get("path", "") for fp in impl_file_plan] if impl_file_plan else []

    return {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "status": "pass",
        "patch_objective":           plan["patch_objective"],
        "source_pass":               plan["source_pass"],
        "target_files":              target_files,
        "patch_sequence":            plan["patch_sequence"],
        "naming_registry":           plan["naming_registry"],
        "animation_contracts":       plan["animation_contracts"],
        "acceptance_signals":        plan["acceptance_signals"],
        "patch_notes":               plan["patch_notes"],
        "implementation_plan_files": implementation_plan_files,
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
