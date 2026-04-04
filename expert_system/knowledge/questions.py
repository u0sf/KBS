# Symptom questions: each answer asserts a fact into working memory.

from __future__ import annotations

from expert_system.domain.models import Question

QUESTIONS: tuple[Question, ...] = (
    Question(
        id="q_life",
        text="When you press the power button, do you see any sign of life\n(fans spinning, LEDs, or sounds)?",
        prerequisites=frozenset(),
        yes_fact="SIGNS_OF_LIFE",
        no_fact="NO_SIGNS_OF_LIFE",
    ),
    Question(
        id="q_psu_led",
        text="Is there any power LED visible on the PSU or motherboard\n(when the PC is plugged in)?",
        prerequisites=frozenset({"NO_SIGNS_OF_LIFE"}),
        yes_fact="PSU_OR_MB_LED_ON",
        no_fact="NO_POWER_LED",
    ),
    Question(
        id="q_fan_spin",
        text="Do the fans spin at all (even briefly) when you power on?",
        prerequisites=frozenset({"NO_SIGNS_OF_LIFE", "PSU_OR_MB_LED_ON"}),
        yes_fact="FANS_SPIN_BRIEFLY",
        no_fact="FANS_DO_NOT_SPIN",
    ),
    Question(
        id="q_display_signal",
        text="Does the monitor show a picture (BIOS logo, boot screen, or desktop)?",
        prerequisites=frozenset({"SIGNS_OF_LIFE"}),
        yes_fact="DISPLAY_HAS_PICTURE",
        no_fact="DISPLAY_NO_PICTURE",
    ),
    Question(
        id="q_cable_swap",
        text="Have you tried a different video cable or another monitor\n(and confirmed the monitor is on and correct input)?",
        prerequisites=frozenset({"SIGNS_OF_LIFE", "DISPLAY_NO_PICTURE"}),
        yes_fact="CABLE_OR_MONITOR_SWAPPED",
        no_fact="NOT_TRIED_CABLE_MONITOR",
    ),
    Question(
        id="q_perf",
        text="Is the system unusually slow, freezing, or taking long to open apps?",
        prerequisites=frozenset({"SIGNS_OF_LIFE", "DISPLAY_HAS_PICTURE"}),
        yes_fact="PERFORMANCE_POOR",
        no_fact="PERFORMANCE_OK",
    ),
    Question(
        id="q_disk_noise",
        text="Do you notice constant loud disk activity or very high disk usage in Task Manager?",
        prerequisites=frozenset(
            {"SIGNS_OF_LIFE", "DISPLAY_HAS_PICTURE", "PERFORMANCE_POOR"}
        ),
        yes_fact="HEAVY_DISK_ACTIVITY",
        no_fact="NO_HEAVY_DISK",
    ),
    Question(
        id="q_thermal",
        text="Does the PC feel very hot, do fans run loud constantly,\nor does it shut down under load?",
        prerequisites=frozenset(
            {"SIGNS_OF_LIFE", "DISPLAY_HAS_PICTURE", "PERFORMANCE_OK"}
        ),
        yes_fact="THERMAL_SYMPTOMS",
        no_fact="NO_THERMAL_SYMPTOMS",
    ),
)
