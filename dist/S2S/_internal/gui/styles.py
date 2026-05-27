import tkinter as tk

from tkinter import ttk


def apply_win95_style(root):

    # ==========================================
    # WINDOW COLORS
    # ==========================================

    bg = "#C0C0C0"

    root.configure(bg=bg)

    style = ttk.Style()

    try:
        style.theme_use("clam")
    except Exception:
        pass

    # ==========================================
    # BUTTONS
    # ==========================================

    style.configure(
        "TButton",
        background=bg,
        foreground="black",
        borderwidth=2,
        relief="raised",
        padding=4
    )

    style.map(
        "TButton",
        relief=[
            ("pressed", "sunken"),
            ("!pressed", "raised")
        ]
    )

    # ==========================================
    # LABELS
    # ==========================================

    style.configure(
        "TLabel",
        background=bg,
        foreground="black"
    )

    # ==========================================
    # FRAME
    # ==========================================

    style.configure(
        "TFrame",
        background=bg
    )

    # ==========================================
    # TREEVIEW
    # ==========================================

    style.configure(
        "Treeview",
        background="white",
        foreground="black",
        fieldbackground="white"
    )

    style.configure(
        "Treeview.Heading",
        background=bg,
        foreground="black",
        relief="raised"
    )

    # ==========================================
    # NOTEBOOK
    # ==========================================

    style.configure(
        "TNotebook",
        background=bg
    )

    style.configure(
        "TNotebook.Tab",
        background=bg,
        padding=[8, 4]
    )