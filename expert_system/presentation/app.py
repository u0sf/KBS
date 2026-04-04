# expert_system/presentation/app.py — Main window: consultation UI + explanation panels.

from __future__ import annotations

import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext
from typing import Callable, Optional

from expert_system.domain.models import KnowledgeBase
from expert_system.inference import ConsultationSession, InferenceResult
from expert_system.knowledge import default_knowledge_base
from expert_system.presentation.theme import Theme


class TroubleshootingApp:
    """
    View/controller for the expert system consultation.
    Separates presentation from inference: only calls ConsultationSession public API.
    """

    def __init__(self) -> None:
        self._kb: KnowledgeBase = default_knowledge_base()
        self.session = ConsultationSession(self._kb)

        self._transition_id: Optional[str] = None
        self._pulse_id: Optional[str] = None
        self._pulse_n = 0

        self.root = tk.Tk()
        self.root.title("Smart Troubleshooting System — Expert System")
        self.root.configure(bg=Theme.bg_root)
        self.root.minsize(960, 640)
        self.root.geometry("1040x700")

        Theme.configure_styles(self.root)
        self._fonts = Theme.fonts(self.root)

        self._build_ui()
        self._start_consultation()

    # --- UI construction -------------------------------------------------

    def _build_ui(self) -> None:
        header = tk.Frame(self.root, bg=Theme.bg_header, height=88)
        header.pack(fill=tk.X)
        header.pack_propagate(False)

        tk.Label(
            header,
            text="Smart Troubleshooting System",
            font=self._fonts["title"],
            fg=Theme.fg,
            bg=Theme.bg_header,
        ).pack(pady=(14, 2))

        tk.Label(
            header,
            text="Knowledge-Based Systems • Forward-chaining production rules • Consultation trace",
            font=self._fonts["subtitle"],
            fg=Theme.fg_muted,
            bg=Theme.bg_header,
        ).pack(pady=(0, 12))

        paned = ttk.Panedwindow(self.root, orient=tk.HORIZONTAL)
        paned.pack(fill=tk.BOTH, expand=True, padx=14, pady=(0, 14))

        left = tk.Frame(paned, bg=Theme.bg_root)
        right = tk.Frame(paned, bg=Theme.bg_panel, highlightthickness=1, highlightbackground=Theme.border)
        paned.add(left, weight=3)
        paned.add(right, weight=2)

        # --- Left: knowledge meta + question + results ---
        meta = tk.Frame(left, bg=Theme.bg_root)
        meta.pack(fill=tk.X, pady=(0, 10))

        self.lbl_kb_title = tk.Label(
            meta,
            text="",
            font=self._fonts["body"],
            fg=Theme.accent,
            bg=Theme.bg_root,
            anchor=tk.W,
        )
        self.lbl_kb_title.pack(fill=tk.X)

        self.lbl_kb_desc = tk.Label(
            meta,
            text="",
            font=self._fonts["small"],
            fg=Theme.fg_muted,
            bg=Theme.bg_root,
            anchor=tk.W,
            wraplength=620,
            justify=tk.LEFT,
        )
        self.lbl_kb_desc.pack(fill=tk.X, pady=(4, 0))

        prog_row = tk.Frame(left, bg=Theme.bg_root)
        prog_row.pack(fill=tk.X, pady=(8, 6))
        self.lbl_progress = tk.Label(
            prog_row,
            text="",
            font=self._fonts["small"],
            fg=Theme.fg_muted,
            bg=Theme.bg_root,
        )
        self.lbl_progress.pack(anchor=tk.W)
        self.progress = ttk.Progressbar(
            prog_row,
            style="STS.Horizontal.TProgressbar",
            mode="determinate",
            maximum=100,
        )
        self.progress.pack(fill=tk.X, pady=(4, 0))

        card = tk.Frame(
            left,
            bg=Theme.bg_card,
            highlightthickness=1,
            highlightbackground=Theme.border,
        )
        card.pack(fill=tk.BOTH, expand=True, pady=(0, 10))

        inner = tk.Frame(card, bg=Theme.bg_card_inner)
        inner.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)

        pad = tk.Frame(inner, bg=Theme.bg_card_inner)
        pad.pack(fill=tk.BOTH, expand=True, padx=22, pady=22)

        self.lbl_phase = tk.Label(
            pad,
            text="",
            font=self._fonts["small"],
            fg=Theme.accent_dim,
            bg=Theme.bg_card_inner,
        )
        self.lbl_phase.pack(pady=(0, 6))

        self.lbl_question = tk.Label(
            pad,
            text="",
            font=self._fonts["question"],
            fg=Theme.fg,
            bg=Theme.bg_card_inner,
            wraplength=560,
            justify=tk.CENTER,
        )
        self.lbl_question.pack(fill=tk.X, pady=(6, 20))

        btn_row = tk.Frame(pad, bg=Theme.bg_card_inner)
        btn_row.pack(pady=8)
        self.btn_yes = self._pill_button(btn_row, "Yes", Theme.success, Theme.success_hover, self._on_yes)
        self.btn_yes.pack(side=tk.LEFT, padx=10)
        self.btn_no = self._pill_button(btn_row, "No", Theme.danger, Theme.danger_hover, self._on_no)
        self.btn_no.pack(side=tk.LEFT, padx=10)

        # Scrollable diagnosis
        self.result_outer = tk.Frame(left, bg=Theme.bg_root)
        self.result_canvas = tk.Canvas(
            self.result_outer,
            bg=Theme.result_bg,
            highlightthickness=2,
            highlightbackground=Theme.result_border,
            height=1,
        )
        self.result_scroll = ttk.Scrollbar(self.result_outer, orient=tk.VERTICAL, command=self.result_canvas.yview)
        self.result_inner = tk.Frame(self.result_canvas, bg=Theme.result_bg)

        def _sync_scroll(_: object = None) -> None:
            self.result_canvas.configure(scrollregion=self.result_canvas.bbox("all"))

        self.result_inner.bind("<Configure>", _sync_scroll)

        self._result_canvas_window = self.result_canvas.create_window(
            (0, 0), window=self.result_inner, anchor=tk.NW
        )
        self.result_canvas.configure(yscrollcommand=self.result_scroll.set)

        def _on_canvas_configure(event: tk.Event) -> None:
            self.result_canvas.itemconfigure(self._result_canvas_window, width=event.width)

        self.result_canvas.bind("<Configure>", _on_canvas_configure)

        self._result_widgets = self._build_result_sections(self.result_inner)

        restart_row = tk.Frame(left, bg=Theme.bg_root)
        restart_row.pack(fill=tk.X, pady=(10, 0))
        self._pill_button(
            restart_row,
            "Restart consultation",
            Theme.neutral,
            Theme.neutral_hover,
            self._restart,
            width=24,
        ).pack()

        # --- Right: working memory + trace ---
        tk.Label(
            right,
            text="Reasoning trace",
            font=self._fonts["body"],
            fg=Theme.accent,
            bg=Theme.bg_panel,
        ).pack(anchor=tk.W, padx=12, pady=(12, 4))

        tk.Label(
            right,
            text="Facts in working memory reflect asserted observations and derived conclusions.",
            font=self._fonts["small"],
            fg=Theme.fg_muted,
            bg=Theme.bg_panel,
            wraplength=320,
            justify=tk.LEFT,
        ).pack(anchor=tk.W, padx=12, pady=(0, 8))

        wm_frame = tk.Frame(right, bg=Theme.bg_trace, highlightthickness=1, highlightbackground=Theme.border)
        wm_frame.pack(fill=tk.X, padx=10, pady=(0, 8))

        tk.Label(
            wm_frame,
            text="Working memory (σ)",
            font=(self._fonts["small"].actual()["family"], 9, "bold"),
            fg=Theme.accent_dim,
            bg=Theme.bg_trace,
        ).pack(anchor=tk.W, padx=8, pady=(6, 2))

        self.list_wm = tk.Listbox(
            wm_frame,
            height=6,
            font=self._fonts["mono"],
            bg="#0f141c",
            fg=Theme.fg,
            selectbackground=Theme.accent_dim,
            borderwidth=0,
            highlightthickness=0,
        )
        self.list_wm.pack(fill=tk.BOTH, expand=True, padx=6, pady=(0, 6))

        tk.Label(
            right,
            text="Consultation log",
            font=(self._fonts["small"].actual()["family"], 9, "bold"),
            fg=Theme.accent_dim,
            bg=Theme.bg_panel,
        ).pack(anchor=tk.W, padx=12, pady=(4, 2))

        self.txt_log = scrolledtext.ScrolledText(
            right,
            height=16,
            font=self._fonts["mono"],
            bg="#0f141c",
            fg=Theme.fg_muted,
            insertbackground=Theme.fg,
            borderwidth=0,
            highlightthickness=1,
            highlightbackground=Theme.border,
            wrap=tk.WORD,
            state=tk.DISABLED,
        )
        self.txt_log.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))

        self.result_canvas.bind("<MouseWheel>", self._on_mousewheel)
        self.result_canvas.bind("<Enter>", lambda _: self.result_canvas.focus_set())

    def _build_result_sections(self, parent: tk.Frame) -> dict[str, tk.Label]:
        widgets: dict[str, tk.Label] = {}
        sections = (
            ("confidence", "Confidence (rule salience heuristic)"),
            ("rule_id", "Fired production rule"),
            ("problem", "Problem"),
            ("solution", "Solution"),
            ("explanation", "Explanation"),
            ("why", "Why this conclusion"),
        )
        for key, title in sections:
            tk.Label(
                parent,
                text=title,
                font=(self._fonts["body"].actual()["family"], 10, "bold"),
                fg=Theme.accent,
                bg=Theme.result_bg,
            ).pack(anchor=tk.W, padx=16, pady=(12, 2))
            lbl = tk.Label(
                parent,
                text="",
                font=self._fonts["body"],
                fg=Theme.fg,
                bg=Theme.result_bg,
                wraplength=520,
                justify=tk.LEFT,
            )
            lbl.pack(fill=tk.X, padx=16, pady=(0, 4))
            widgets[key] = lbl
        return widgets

    def _pill_button(
        self,
        parent: tk.Widget,
        text: str,
        bg: str,
        hover: str,
        command: Callable[[], None],
        width: int = 14,
    ) -> tk.Button:
        btn = tk.Button(
            parent,
            text=text,
            font=(self._fonts["body"].actual()["family"], 12, "bold"),
            fg=Theme.fg,
            bg=bg,
            activebackground=hover,
            activeforeground=Theme.fg,
            relief=tk.FLAT,
            padx=22,
            pady=12,
            width=width,
            cursor="hand2",
            command=command,
        )

        def enter(_: object) -> None:
            btn.configure(bg=hover)

        def leave(_: object) -> None:
            btn.configure(bg=bg)

        btn.bind("<Enter>", enter)
        btn.bind("<Leave>", leave)
        return btn

    def _on_mousewheel(self, event: tk.Event) -> None:
        if self.result_canvas.winfo_exists() and event.delta:
            self.result_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    # --- Session flow ------------------------------------------------------

    def _cancel_timers(self) -> None:
        if self._transition_id is not None:
            self.root.after_cancel(self._transition_id)
            self._transition_id = None
        if self._pulse_id is not None:
            self.root.after_cancel(self._pulse_id)
            self._pulse_id = None

    def _start_consultation(self) -> None:
        self.session.reset()
        self._cancel_timers()
        self.lbl_kb_title.configure(text=self._kb.title)
        self.lbl_kb_desc.configure(text=self._kb.description)
        self.result_outer.pack_forget()
        self._set_buttons(True)
        self._refresh_side_panels()
        self._update_progress()
        self._show_question(immediate=True)

    def _answered_count(self) -> int:
        return sum(1 for q in self._kb.questions if self.session.engine.question_answered(q))

    def _update_progress(self) -> None:
        total = len(self._kb.questions)
        done = self._answered_count()
        self.lbl_progress.configure(text=f"Acquisition step: {done} answered • up to {total} symptom questions in KB")
        pct = min(100, int(done / max(total, 1) * 100))
        self.progress.configure(value=pct)

    def _refresh_side_panels(self) -> None:
        self.list_wm.delete(0, tk.END)
        for fact in self.session.working_memory_lines():
            self.list_wm.insert(tk.END, fact)

        self.txt_log.configure(state=tk.NORMAL)
        self.txt_log.delete("1.0", tk.END)
        self.txt_log.insert(tk.END, self.session.log_text())
        self.txt_log.configure(state=tk.DISABLED)
        self.txt_log.see(tk.END)

    def _set_buttons(self, enabled: bool) -> None:
        state = tk.NORMAL if enabled else tk.DISABLED
        self.btn_yes.configure(state=state)
        self.btn_no.configure(state=state)

    def _show_question(self, immediate: bool = False) -> None:
        q = self.session.current_question()
        if q is None:
            self.lbl_phase.configure(text="Consultation state")
            self.lbl_question.configure(
                text="No further symptom questions apply.\nUse Restart if you want a new consultation.",
                fg=Theme.fg_muted,
            )
            self._set_buttons(False)
            return

        def apply() -> None:
            self.lbl_phase.configure(text=f"Symptom acquisition • {q.id}")
            self.lbl_question.configure(fg=Theme.fg, text=q.text)
            self._set_buttons(True)
            self._update_progress()

        if immediate:
            apply()
        else:
            self.lbl_question.configure(fg=Theme.fg_muted)
            self.lbl_phase.configure(text="Inference cycle complete — next question")
            self._set_buttons(False)
            self._transition_id = self.root.after(200, apply)

    def _on_yes(self) -> None:
        self._submit(True)

    def _on_no(self) -> None:
        self._submit(False)

    def _submit(self, yes: bool) -> None:
        result = self.session.submit_boolean_answer(yes)
        self._refresh_side_panels()
        self._update_progress()

        if result.diagnosis:
            self._show_diagnosis(result)
        else:
            self._show_question(immediate=False)

    def _show_diagnosis(self, result: InferenceResult) -> None:
        self._cancel_timers()
        self._set_buttons(False)
        dx = result.diagnosis
        assert dx is not None

        self.lbl_phase.configure(text="Consultation complete — conclusion reached")
        self.lbl_question.configure(text="Diagnosis", fg=Theme.accent)

        fired = result.fired_rule
        rule_label = fired.rule_id if fired and fired.rule_id else "(unnamed rule in base)"

        self._result_widgets["confidence"].configure(
            text=f"{int(round(result.confidence * 100))}% — based on conjunction size in the fired rule (demo heuristic)."
        )
        self._result_widgets["rule_id"].configure(text=rule_label)
        self._result_widgets["problem"].configure(text=dx.problem)
        self._result_widgets["solution"].configure(text=dx.solution)
        self._result_widgets["explanation"].configure(text=dx.explanation)

        why_parts = []
        if result.matched_conditions:
            why_parts.append("Matched conditions (antecedents):\n• " + "\n• ".join(result.matched_conditions))
        if dx.supporting_fact_hints:
            why_parts.append("Supporting observations:\n• " + "\n• ".join(dx.supporting_fact_hints))
        if result.derived_facts:
            why_parts.append("Derived facts this cycle:\n• " + "\n• ".join(result.derived_facts))
        self._result_widgets["why"].configure(text="\n\n".join(why_parts) if why_parts else "—")

        self.result_outer.pack(fill=tk.BOTH, expand=True, pady=(0, 6))
        self.result_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.result_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.root.update_idletasks()
        self.result_canvas.configure(scrollregion=self.result_canvas.bbox("all"))
        self._pulse_border()

    def _pulse_border(self) -> None:
        self._pulse_n = 0

        def step() -> None:
            self._pulse_n += 1
            if self._pulse_n > 8:
                self.result_canvas.configure(highlightbackground=Theme.result_border)
                self._pulse_id = None
                return
            hi = Theme.result_border if self._pulse_n % 2 else Theme.accent_dim
            self.result_canvas.configure(highlightbackground=hi)
            self._pulse_id = self.root.after(650, step)

        self._pulse_id = self.root.after(300, step)

    def _restart(self) -> None:
        self._cancel_timers()
        self.result_outer.pack_forget()
        self._start_consultation()

    def run(self) -> None:
        self.root.mainloop()


def launch_app() -> None:
    TroubleshootingApp().run()
