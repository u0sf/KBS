# Visual theme tokens — single place for colours and typography (presentation layer).

from __future__ import annotations

import tkinter as tk
from tkinter import font as tkfont
from tkinter import ttk


class Theme:
    """Soft dark palette with readable contrast (academic / demo friendly)."""

    bg_root = "#141c2b"
    bg_header = "#0f1624"
    bg_panel = "#1c2738"
    bg_card = "#222e42"
    bg_card_inner = "#263449"
    bg_trace = "#182030"
    fg = "#e8edf4"
    fg_muted = "#8b9cb5"
    accent = "#6eb3e8"
    accent_dim = "#4a8cc4"
    success = "#2f8f6a"
    success_hover = "#3aaf82"
    danger = "#c45c6a"
    danger_hover = "#d4727f"
    neutral = "#3d5270"
    neutral_hover = "#4e6585"
    border = "#334155"
    result_bg = "#1a3d52"
    result_border = "#6eb3e8"

    @staticmethod
    def configure_styles(root: tk.Tk) -> ttk.Style:
        s = ttk.Style(root)
        try:
            s.theme_use("clam")
        except tk.TclError:
            pass
        s.configure(
            "STS.Horizontal.TProgressbar",
            troughcolor=Theme.bg_card_inner,
            background=Theme.accent,
            thickness=6,
        )
        return s

    @staticmethod
    def fonts(root: tk.Tk) -> dict[str, tkfont.Font]:
        fam = "Segoe UI"
        try:
            tkfont.Font(family=fam, size=1)
        except tk.TclError:
            fam = "TkDefaultFont"
        return {
            "title": tkfont.Font(root, family=fam, size=20, weight="bold"),
            "subtitle": tkfont.Font(root, family=fam, size=10),
            "question": tkfont.Font(root, family=fam, size=14),
            "body": tkfont.Font(root, family=fam, size=11),
            "small": tkfont.Font(root, family=fam, size=9),
            "mono": tkfont.Font(root, family="Consolas", size=9),
        }
