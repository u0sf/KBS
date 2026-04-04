# Terminal conclusions (goal hypotheses) keyed by rule consequent DX:... identifiers.

from __future__ import annotations

from expert_system.domain.models import Diagnosis

DIAGNOSES: dict[str, Diagnosis] = {
    "DX_PSU_CABLE": Diagnosis(
        problem="Power supply or power delivery failure",
        solution=(
            "Check the wall outlet, power strip, and PSU power switch. Reseat the 24-pin "
            "and CPU power cables on the motherboard. If still dead, test with a known-good "
            "PSU or replace the unit."
        ),
        explanation=(
            "No signs of life with no PSU/motherboard LED strongly suggests no usable power "
            "reaching the system (cable, outlet, or failed PSU)."
        ),
        supporting_fact_hints=("No fans/LEDs when powering on", "No PSU or board power LED"),
    ),
    "DX_MOTHERBOARD_SHORT": Diagnosis(
        problem="Possible motherboard fault, short, or failed component",
        solution=(
            "Disconnect non-essential devices, reseat RAM and GPU, clear CMOS if documented "
            "for your board. If LED is present but fans never spin, seek professional "
            "diagnostics or board/PSU swap testing."
        ),
        explanation=(
            "Power LED present but no fan movement suggests some standby power but the "
            "system is not starting the boot sequence normally."
        ),
        supporting_fact_hints=("No signs of life", "Power LED visible", "Fans do not spin"),
    ),
    "DX_DISPLAY_PATH": Diagnosis(
        problem="Display output path issue (cable, monitor, port, or graphics)",
        solution=(
            "Try another cable and input port, verify monitor source/input. If integrated "
            "graphics exists, test without discrete GPU. Update GPU drivers from safe mode "
            "if you can reach it, or reseat the graphics card."
        ),
        explanation=(
            "The PC appears to run but there is no stable picture even after cable/monitor "
            "checks — likely display chain or GPU-related."
        ),
        supporting_fact_hints=("System seems on", "No picture", "Cable/monitor swap tried"),
    ),
    "DX_DISPLAY_BASIC": Diagnosis(
        problem="Likely cable, monitor input, or loose video connection",
        solution=(
            "Double-check monitor power and input source. Reseat the video cable at both "
            "ends; try another cable or monitor if available."
        ),
        explanation=(
            "There is no picture but you have not yet ruled out cable/monitor issues — "
            "most display problems start there."
        ),
        supporting_fact_hints=("No picture", "Cable/monitor not yet ruled out"),
    ),
    "DX_STORAGE_PERF": Diagnosis(
        problem="Performance bottleneck — storage or background load",
        solution=(
            "Check Task Manager for disk at 100%. Consider freeing space, disabling heavy "
            "startup apps, scanning for malware, and upgrading to an SSD if still on a slow HDD."
        ),
        explanation=(
            "Poor performance together with heavy disk activity points to storage saturation, "
            "failing drive, or excessive background I/O."
        ),
        supporting_fact_hints=("Slow / freezing", "Heavy disk activity reported"),
    ),
    "DX_RAM_SOFTWARE": Diagnosis(
        problem="RAM pressure, software, or thermal throttling (non-disk)",
        solution=(
            "Close unused programs, check RAM usage in Task Manager, run a reputable "
            "malware scan, update drivers/OS, and ensure adequate cooling. Consider adding RAM "
            "if consistently near capacity."
        ),
        explanation=(
            "Performance issues without dominant disk symptoms often involve memory pressure, "
            "background software, or CPU throttling."
        ),
        supporting_fact_hints=("Poor performance", "No heavy disk pattern"),
    ),
    "DX_OVERHEATING": Diagnosis(
        problem="Overheating or inadequate cooling",
        solution=(
            "Clean dust from heatsinks and fans, replace dried thermal paste on CPU if "
            "comfortable doing so, improve case airflow, and verify all fans spin. Use "
            "hardware monitor tools to check temperatures under load."
        ),
        explanation=(
            "You reported heat-related symptoms while general performance seemed otherwise OK — "
            "thermal limits may be causing throttling or shutdowns."
        ),
        supporting_fact_hints=("Normal perceived speed", "Heat / loud fans / shutdowns under load"),
    ),
    "DX_GENERAL_HEALTHY": Diagnosis(
        problem="No strong fault pattern detected from answers",
        solution=(
            "Keep drivers and Windows updated, run periodic disk cleanup, and monitor "
            "temperatures. If a specific symptom appears later, run this troubleshooter again."
        ),
        explanation=(
            "Signs of life and display were OK, performance felt fine, and no thermal pattern "
            "was reported — no rule fired a hardware fault with high specificity."
        ),
        supporting_fact_hints=("System appears operational from described symptoms",),
    ),
}
