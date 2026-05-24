import tkinter as tk

from tkinter import filedialog
from tkinter import messagebox

from tksheet import Sheet

from speech.recorder import SpeechRecorder

from spreadsheet.spreadsheet_model import (
    SpreadsheetModel
)

from spreadsheet.spreadsheet_io import (
    SpreadsheetIO
)

from spreadsheet.conditional_formatting import (
    ConditionalFormattingRule
)


class MainWindow:

    def __init__(self, root):

        self.root = root

        self.root.title(
            "Speech to Spreadsheet"
        )

        self.root.geometry("1200x700")

        self.model = SpreadsheetModel()

        self.recorder = SpeechRecorder(
            callback=self.on_transcript
        )

        self.is_recording = False

        self.build_ui()

    # ==========================================
    # UI
    # ==========================================

    def build_ui(self):

        toolbar = tk.Frame(self.root)

        toolbar.pack(fill=tk.X)

        tk.Button(
            toolbar,
            text="Create Spreadsheet",
            command=self.create_spreadsheet
        ).pack(side=tk.LEFT)

        tk.Button(
            toolbar,
            text="Open Spreadsheet",
            command=self.open_spreadsheet
        ).pack(side=tk.LEFT)

        tk.Button(
            toolbar,
            text="Save Spreadsheet",
            command=self.save_spreadsheet
        ).pack(side=tk.LEFT)

        tk.Button(
            toolbar,
            text="Add Highlight Rule",
            command=self.add_rule
        ).pack(side=tk.LEFT)

        self.dictation_button = tk.Button(
            self.root,
            text="START DICTATION",
            font=("Arial", 26, "bold"),
            height=3,
            bg="green",
            fg="white",
            command=self.toggle_recording
        )

        self.dictation_button.pack(
            fill=tk.X,
            pady=10
        )

        self.sheet = Sheet(
            self.root,
            data=[[""] * 20 for _ in range(50)]
        )

        self.sheet.enable_bindings()

        self.sheet.pack(
            fill=tk.BOTH,
            expand=True
        )

    # ==========================================
    # CREATE
    # ==========================================

    def create_spreadsheet(self):

        self.model = SpreadsheetModel()

        self.refresh_sheet()

    # ==========================================
    # OPEN
    # ==========================================

    def open_spreadsheet(self):

        path = filedialog.askopenfilename(
            filetypes=[
                ("Spreadsheet", "*.xlsx *.ods")
            ]
        )

        if not path:
            return

        try:

            df, formatting = (
                SpreadsheetIO.load(path)
            )

            self.model.df = df

            self.refresh_sheet()

            # APPLY EXISTING FORMATTING

            for (
                row,
                col
            ), color in formatting.items():

                self.sheet.highlight_cells(
                    row=row,
                    column=col,
                    bg="yellow"
                )

        except Exception as e:

            messagebox.showerror(
                "Open Error",
                str(e)
            )

    # ==========================================
    # SAVE
    # ==========================================

    def save_spreadsheet(self):

        path = filedialog.asksaveasfilename(
            defaultextension=".xlsx",
            filetypes=[
                ("Excel", "*.xlsx")
            ]
        )

        if not path:
            return

        self.sync_sheet_to_model()

        SpreadsheetIO.save_xlsx(
            self.model,
            path
        )

        messagebox.showinfo(
            "Saved",
            "Spreadsheet saved successfully."
        )

    # ==========================================
    # DICTATION
    # ==========================================

    def toggle_recording(self):

        if self.is_recording:

            self.recorder.stop()

            self.is_recording = False

            self.dictation_button.config(
                text="START DICTATION",
                bg="green"
            )

        else:

            self.recorder.start()

            self.is_recording = True

            self.dictation_button.config(
                text="STOP DICTATION",
                bg="red"
            )

    # ==========================================
    # TRANSCRIPT
    # ==========================================

    def on_transcript(self, text):

        self.root.after(
            0,
            lambda: self.process_transcript(text)
        )

        row = self.model.current_row
        col = self.model.current_col

        self.model.set_cell(
            row,
            col,
            text
        )

        self.sheet.set_cell_data(
            row,
            col,
            text
        )

        self.model.current_col += 1
    
    def process_transcript(self, text):

        row = self.model.current_row
        col = self.model.current_col

        self.model.set_cell(
            row,
            col,
            text
        )

        self.sheet.set_cell_data(
            row,
            col,
            text
        )

        self.model.current_col += 1

    # ==========================================
    # RULES
    # ==========================================

    def add_rule(self):

        rule = ConditionalFormattingRule(
            column=0,
            operator=">",
            value=10
        )

        self.model.add_rule(rule)

        messagebox.showinfo(
            "Rule Added",
            "Conditional formatting rule added."
        )

    # ==========================================
    # REFRESH
    # ==========================================

    def refresh_sheet(self):

        data = self.model.df.fillna("").values.tolist()

        self.sheet.set_sheet_data(data)

    # ==========================================
    # SYNC
    # ==========================================

    def sync_sheet_to_model(self):

        data = self.sheet.get_sheet_data()

        import pandas as pd

        self.model.df = pd.DataFrame(data)