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
