"""
Prototype UI Spec Agent — Stage 8.

Translates an approved prototype_build_spec into a UI-ready specification
with screen layouts, component styling, animations, and accessibility requirements.

Modes:
    Stub: deterministic keyword-based templates (concept overrides + generic fallback).
    LLM:  model_callable replaces the stub.
"""
from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict

from utils.shared_agent_runner import AgentSpec, SharedAgentRunner

# ---------------------------------------------------------------------------
# Concept-specific overrides — rich, UI-ready specifications
# ---------------------------------------------------------------------------

CONCEPT_OVERRIDES: Dict[str, Dict[str, Any]] = {
    "bakery": {
        "ui_objective": (
            "Create an accessible, child-friendly UI for a K-2 bakery addition game "
            "with clear visual feedback, large touch targets, and satisfying animations "
            "that reinforce the mathematical learning loop."
        ),
        "screen_layouts": [
            {
                "screen_id": "bakery_round",
                "screen_name": "Bakery Round Screen",
                "layout_type": "single_column",
                "regions": [
                    {
                        "region_id": "header",
                        "region_name": "Game Header",
                        "position": "top: 0; left: 0; right: 0; height: 80px",
                        "size": "100% width, 80px height",
                        "purpose": "Shows customer order and current progress"
                    },
                    {
                        "region_id": "play_area",
                        "region_name": "Main Play Area",
                        "position": "top: 80px; bottom: 100px; left: 20px; right: 20px",
                        "size": "calc(100% - 40px) width, calc(100% - 180px) height",
                        "purpose": "Interactive pastry selection and box area"
                    },
                    {
                        "region_id": "footer",
                        "region_name": "Round Footer",
                        "position": "bottom: 0; left: 0; right: 0; height: 100px",
                        "size": "100% width, 100px height",
                        "purpose": "Round progress and next round button"
                    }
                ]
            }
        ],
        "ui_components": [
            {
                "component_id": "pastry_button",
                "component_name": "Pastry Selection Button",
                "component_type": "interactive",
                "visual_style": {
                    "colors": {
                        "primary": "#FFB74D",
                        "secondary": "#FF9800",
                        "accent": "#FFC107",
                        "background": "#FFF8E1"
                    },
                    "typography": {
                        "font_family": "Comic Sans MS, cursive",
                        "font_size": "24px",
                        "font_weight": "bold"
                    },
                    "spacing": {
                        "padding": "20px",
                        "margin": "10px"
                    }
                },
                "interaction_states": ["default", "hover", "active", "success"],
                "accessibility": {
                    "aria_label": "Add {pastry_type} to order",
                    "keyboard_navigation": True,
                    "screen_reader_support": True,
                    "color_contrast_ratio": 4.5
                }
            },
            {
                "component_id": "order_display",
                "component_name": "Customer Order Display",
                "component_type": "display",
                "visual_style": {
                    "colors": {
                        "primary": "#4CAF50",
                        "secondary": "#388E3C",
                        "background": "#E8F5E8"
                    },
                    "typography": {
                        "font_family": "Arial, sans-serif",
                        "font_size": "28px",
                        "font_weight": "bold"
                    },
                    "spacing": {
                        "padding": "15px",
                        "margin": "10px"
                    }
                },
                "interaction_states": ["default"],
                "accessibility": {
                    "aria_label": "Customer wants {target_number} pastries",
                    "keyboard_navigation": False,
                    "screen_reader_support": True,
                    "color_contrast_ratio": 4.5
                }
            }
        ],
        "animations_and_transitions": [
            {
                "animation_id": "pastry_add",
                "animation_name": "Pastry Addition Animation",
                "trigger": "When player taps a pastry to add to order",
                "duration": "0.3s",
                "easing": "ease-out",
                "description": "Pastry scales up 10% then flies to the box with a bounce effect"
            },
            {
                "animation_id": "success_burst",
                "animation_name": "Order Complete Success",
                "trigger": "When order total matches target exactly",
                "duration": "0.8s",
                "easing": "ease-out",
                "description": "Box glows green, confetti particles burst, customer smiles and waves"
            },
            {
                "animation_id": "overshoot_bounce",
                "animation_name": "Overshoot Correction",
                "trigger": "When order total exceeds target",
                "duration": "0.5s",
                "easing": "ease-in-out",
                "description": "Last pastry bounces back out of box with red flash, total decrements"
            }
        ],
        "responsive_breakpoints": [
            {
                "breakpoint_name": "tablet",
                "min_width": "768px",
                "max_width": "1024px",
                "layout_adjustments": [
                    "Increase button sizes by 20%",
                    "Adjust spacing for larger screens",
                    "Center play area with max-width constraint"
                ]
            },
            {
                "breakpoint_name": "desktop",
                "min_width": "1025px",
                "layout_adjustments": [
                    "Use grid layout instead of single column",
                    "Add side panels for additional information",
                    "Maintain touch-friendly sizing for hybrid devices"
                ]
            }
        ],
        "accessibility_requirements": {
            "wcag_level": "AA",
            "keyboard_navigation_complete": True,
            "screen_reader_compatible": True,
            "color_blind_friendly": True,
            "motor_impairment_considerations": [
                "Large touch targets (minimum 44px)",
                "No time pressure for motor actions",
                "Clear visual feedback for all interactions",
                "Alternative input methods supported"
            ]
        }
    }
}


def _generic_ui_spec(job_id: str, concept_keywords: list[str]) -> Dict[str, Any]:
    """Generic fallback UI spec when no concept override exists."""
    return {
        "ui_objective": (
            "Create a clean, accessible UI specification that supports the core learning "
            "interaction with appropriate visual hierarchy, feedback systems, and inclusive design."
        ),
        "screen_layouts": [
            {
                "screen_id": "main_game",
                "screen_name": "Main Game Screen",
                "layout_type": "single_column",
                "regions": [
                    {
                        "region_id": "header",
                        "region_name": "Header Area",
                        "position": "top: 0; left: 0; right: 0; height: 15%",
                        "size": "100% width, 15% height",
                        "purpose": "Display progress and objectives"
                    },
                    {
                        "region_id": "content",
                        "region_name": "Main Content Area",
                        "position": "top: 15%; bottom: 20%; left: 5%; right: 5%",
                        "size": "90% width, 65% height",
                        "purpose": "Primary interactive elements"
                    },
                    {
                        "region_id": "footer",
                        "region_name": "Footer Area",
                        "position": "bottom: 0; left: 0; right: 0; height: 20%",
                        "size": "100% width, 20% height",
                        "purpose": "Controls and feedback"
                    }
                ]
            }
        ],
        "ui_components": [
            {
                "component_id": "primary_action",
                "component_name": "Primary Action Button",
                "component_type": "interactive",
                "visual_style": {
                    "colors": {
                        "primary": "#2196F3",
                        "secondary": "#1976D2",
                        "accent": "#42A5F5",
                        "background": "#FFFFFF"
                    },
                    "typography": {
                        "font_family": "Arial, sans-serif",
                        "font_size": "16px",
                        "font_weight": "bold"
                    },
                    "spacing": {
                        "padding": "12px 24px",
                        "margin": "8px"
                    }
                },
                "interaction_states": ["default", "hover", "active", "disabled"],
                "accessibility": {
                    "aria_label": "Perform main action",
                    "keyboard_navigation": True,
                    "screen_reader_support": True,
                    "color_contrast_ratio": 4.5
                }
            }
        ],
        "animations_and_transitions": [
            {
                "animation_id": "state_change",
                "animation_name": "State Change Transition",
                "trigger": "When game state changes",
                "duration": "0.3s",
                "easing": "ease-in-out",
                "description": "Smooth transition between different UI states"
            }
        ],
        "responsive_breakpoints": [
            {
                "breakpoint_name": "mobile",
                "max_width": "767px",
                "layout_adjustments": [
                    "Stack elements vertically",
                    "Increase touch target sizes",
                    "Simplify layout for small screens"
                ]
            }
        ],
        "accessibility_requirements": {
            "wcag_level": "AA",
            "keyboard_navigation_complete": True,
            "screen_reader_compatible": True,
            "color_blind_friendly": True,
            "motor_impairment_considerations": [
                "Minimum 44px touch targets",
                "No gesture-only interactions",
                "Clear visual focus indicators"
            ]
        }
    }


def run(
    job_id: str,
    repo_root: Path,
    model_callable: Any = None,
) -> Dict[str, Any]:
    """
    Run the Prototype UI Spec Agent.

    Args:
        job_id: Job workspace identifier
        repo_root: Repository root path
        model_callable: Optional LLM callable for non-stub mode

    Returns:
        Validated prototype_ui_spec artifact
    """
    agent_spec = AgentSpec(
        agent_name="Prototype UI Spec Agent",
        input_artifacts=["prototype_build_spec"],
        output_artifact="prototype_ui_spec",
        prompt_template_path=repo_root / "agents" / "prototype_ui_spec" / "prompt.md",
        config_path=repo_root / "agents" / "prototype_ui_spec" / "config.yaml",
        concept_overrides=CONCEPT_OVERRIDES,
        generic_fallback=_generic_ui_spec,
    )

    runner = SharedAgentRunner(
        agent_spec=agent_spec,
        job_id=job_id,
        repo_root=repo_root,
        model_callable=model_callable,
    )

    return runner.run()