# IF–THEN production rules for forward chaining (rule base R1…Rn).

from __future__ import annotations

from typing import Tuple

from expert_system.domain.models import ProductionRule


def _labels(*pairs: Tuple[str, str]) -> Tuple[Tuple[str, str], ...]:
    return pairs


CORE_RULES: tuple[ProductionRule, ...] = (
    ProductionRule(
        frozenset({"NO_SIGNS_OF_LIFE", "NO_POWER_LED"}),
        "DX:DX_PSU_CABLE",
        _labels(
            ("NO_SIGNS_OF_LIFE", "No signs of life when pressing power"),
            ("NO_POWER_LED", "No PSU/motherboard power LED"),
        ),
        rule_id="R1_POWER_NO_LED",
    ),
    ProductionRule(
        frozenset({"NO_SIGNS_OF_LIFE", "PSU_OR_MB_LED_ON", "FANS_DO_NOT_SPIN"}),
        "DX:DX_MOTHERBOARD_SHORT",
        _labels(
            ("NO_SIGNS_OF_LIFE", "No signs of life"),
            ("PSU_OR_MB_LED_ON", "Power LED visible"),
            ("FANS_DO_NOT_SPIN", "Fans do not spin"),
        ),
        rule_id="R2_LED_NO_FAN",
    ),
    ProductionRule(
        frozenset({"NO_SIGNS_OF_LIFE", "PSU_OR_MB_LED_ON", "FANS_SPIN_BRIEFLY"}),
        "FACT:POWER_SUBSYSTEM_AMBIGUOUS",
        (),
        rule_id="R3_DERIVE_AMBIGUOUS_POWER",
    ),
    ProductionRule(
        frozenset({"SIGNS_OF_LIFE", "DISPLAY_NO_PICTURE", "CABLE_OR_MONITOR_SWAPPED"}),
        "DX:DX_DISPLAY_PATH",
        _labels(
            ("SIGNS_OF_LIFE", "System shows signs of powering on"),
            ("DISPLAY_NO_PICTURE", "No picture on screen"),
            ("CABLE_OR_MONITOR_SWAPPED", "Cable/monitor swap attempted"),
        ),
        rule_id="R4_DISPLAY_AFTER_SWAP",
    ),
    ProductionRule(
        frozenset({"SIGNS_OF_LIFE", "DISPLAY_NO_PICTURE", "NOT_TRIED_CABLE_MONITOR"}),
        "DX:DX_DISPLAY_BASIC",
        _labels(
            ("SIGNS_OF_LIFE", "System shows signs of life"),
            ("DISPLAY_NO_PICTURE", "No picture"),
            ("NOT_TRIED_CABLE_MONITOR", "Cable/monitor not fully ruled out"),
        ),
        rule_id="R5_DISPLAY_BASIC",
    ),
    ProductionRule(
        frozenset(
            {
                "SIGNS_OF_LIFE",
                "DISPLAY_HAS_PICTURE",
                "PERFORMANCE_POOR",
                "HEAVY_DISK_ACTIVITY",
            }
        ),
        "DX:DX_STORAGE_PERF",
        _labels(
            ("PERFORMANCE_POOR", "Poor performance"),
            ("HEAVY_DISK_ACTIVITY", "Heavy disk activity"),
        ),
        rule_id="R6_STORAGE_PERF",
    ),
    ProductionRule(
        frozenset(
            {
                "SIGNS_OF_LIFE",
                "DISPLAY_HAS_PICTURE",
                "PERFORMANCE_POOR",
                "NO_HEAVY_DISK",
            }
        ),
        "DX:DX_RAM_SOFTWARE",
        _labels(
            ("PERFORMANCE_POOR", "Poor performance"),
            ("NO_HEAVY_DISK", "Disk not the dominant symptom"),
        ),
        rule_id="R7_RAM_SOFTWARE",
    ),
    ProductionRule(
        frozenset(
            {
                "SIGNS_OF_LIFE",
                "DISPLAY_HAS_PICTURE",
                "PERFORMANCE_OK",
                "THERMAL_SYMPTOMS",
            }
        ),
        "DX:DX_OVERHEATING",
        _labels(
            ("PERFORMANCE_OK", "General speed acceptable"),
            ("THERMAL_SYMPTOMS", "Heat / noise / shutdown pattern"),
        ),
        rule_id="R8_THERMAL",
    ),
    ProductionRule(
        frozenset(
            {
                "SIGNS_OF_LIFE",
                "DISPLAY_HAS_PICTURE",
                "PERFORMANCE_OK",
                "NO_THERMAL_SYMPTOMS",
            }
        ),
        "DX:DX_GENERAL_HEALTHY",
        _labels(
            ("SIGNS_OF_LIFE", "System powers and responds"),
            ("DISPLAY_HAS_PICTURE", "Display works"),
            ("PERFORMANCE_OK", "No major slowdown reported"),
            ("NO_THERMAL_SYMPTOMS", "No overheating pattern"),
        ),
        rule_id="R9_NO_FAULT_PATTERN",
    ),
)

AMBIGUOUS_POWER_RULE = ProductionRule(
    frozenset({"POWER_SUBSYSTEM_AMBIGUOUS"}),
    "DX:DX_MOTHERBOARD_SHORT",
    _labels(
        ("POWER_SUBSYSTEM_AMBIGUOUS", "Partial power/fan activity but unclear boot"),
    ),
    rule_id="R10_AMBIGUOUS_TO_MOBO",
)


def ordered_production_rules() -> tuple[ProductionRule, ...]:
    """Full rule list: core rules first, then follow-up rules that depend on derived facts."""
    return CORE_RULES + (AMBIGUOUS_POWER_RULE,)
