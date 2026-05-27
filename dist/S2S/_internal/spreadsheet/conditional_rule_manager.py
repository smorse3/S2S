import tkinter as tk

from tkinter import ttk
from tkinter import colorchooser

from spreadsheet.conditional_formatting import (
    ConditionalFormattingRule
)


class ConditionalRuleManager:

    def __init__(
        self,
        parent,
        model,
        refresh_callback
    ):

        self.model = model

        self.refresh_callback = (
            refresh_callback
        )

        self.window = tk.Toplevel(parent)

        self.window.title(
            "Conditional Formatting Rules"
        )

        self.window.geometry("700x500")

        self.build_ui()

    # =====================================
    # UI
    # =====================================

    def build_ui(self):

        top = tk.Frame(self.window)

        top.pack(
            fill=tk.BOTH,
            expand=True,
            padx=10,
            pady=10
        )

        # ---------------------------------
        # RULE LIST
        # ---------------------------------

        self.rule_list = tk.Listbox(
            top,
            height=10
        )

        self.rule_list.pack(
            fill=tk.X
        )

        self.refresh_rule_list()

        # ---------------------------------
        # EDITOR
        # ---------------------------------

        editor = tk.LabelFrame(
            top,
            text="Rule"
        )

        editor.pack(
            fill=tk.X,
            pady=10
        )

        # RULE TYPE

        tk.Label(
            editor,
            text="Rule Type"
        ).grid(
            row=0,
            column=0,
            sticky="w"
        )

        self.rule_type = ttk.Combobox(
            editor,
            values=[
                "between",
                "not_between",
                "greater_than",
                "less_than",
                "equal",
                "contains",
                "blank",
                "not_blank"
            ]
        )

        self.rule_type.set("between")

        self.rule_type.grid(
            row=0,
            column=1
        )

        # MIN

        tk.Label(
            editor,
            text="Min"
        ).grid(
            row=1,
            column=0
        )

        self.min_entry = tk.Entry(editor)

        self.min_entry.grid(
            row=1,
            column=1
        )

        # MAX

        tk.Label(
            editor,
            text="Max"
        ).grid(
            row=2,
            column=0
        )

        self.max_entry = tk.Entry(editor)

        self.max_entry.grid(
            row=2,
            column=1
        )

        # VALUE

        tk.Label(
            editor,
            text="Value"
        ).grid(
            row=3,
            column=0
        )

        self.value_entry = tk.Entry(editor)

        self.value_entry.grid(
            row=3,
            column=1
        )

        # RANGE

        tk.Label(
            editor,
            text="Applies To"
        ).grid(
            row=4,
            column=0
        )

        self.range_entry = tk.Entry(editor)

        self.range_entry.insert(
            0,
            "A1:Z100"
        )

        self.range_entry.grid(
            row=4,
            column=1
        )

        # COLOR

        self.color = "#FFFF00"

        tk.Button(
            editor,
            text="Select Color",
            command=self.choose_color
        ).grid(
            row=5,
            column=0,
            pady=5
        )

        # BUTTONS

        tk.Button(
            editor,
            text="Add Rule",
            command=self.add_rule
        ).grid(
            row=6,
            column=0,
            pady=10
        )

        tk.Button(
            editor,
            text="Delete Selected",
            command=self.delete_rule
        ).grid(
            row=6,
            column=1,
            pady=10
        )

    # =====================================
    # COLOR
    # =====================================

    def choose_color(self):

        color = colorchooser.askcolor()[1]

        if color:

            self.color = color

    # =====================================
    # ADD
    # =====================================

    def add_rule(self):

        rule = ConditionalFormattingRule(

            rule_type=(
                self.rule_type.get()
            ),

            min_value=(
                float(
                    self.min_entry.get()
                )
                if self.min_entry.get()
                else None
            ),

            max_value=(
                float(
                    self.max_entry.get()
                )
                if self.max_entry.get()
                else None
            ),

            value=self.value_entry.get(),

            color=self.color,

            target_range=(
                self.range_entry.get()
            )
        )

        self.model.add_rule(rule)

        self.refresh_rule_list()

        self.refresh_callback()

    # =====================================
    # DELETE
    # =====================================

    def delete_rule(self):

        selection = (
            self.rule_list.curselection()
        )

        if not selection:
            return

        index = selection[0]

        self.model.remove_rule(index)

        self.refresh_rule_list()

        self.refresh_callback()

    # =====================================
    # REFRESH
    # =====================================

    def refresh_rule_list(self):

        self.rule_list.delete(
            0,
            tk.END
        )

        for rule in (
            self.model.conditional_rules
        ):

            self.rule_list.insert(
                tk.END,
                (
                    f"{rule.rule_type} | "
                    f"{rule.target_range}"
                )
            )