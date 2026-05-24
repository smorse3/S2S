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

    # ==================================================
    # INIT
    # ==================================================

    def __init__(self, root):

        self.root = root

        self.root.title(
            "Speech to Spreadsheet"
        )

        self.root.geometry("1200x700")

        # ----------------------------------------------
        # MODEL
        # ----------------------------------------------

        self.model = SpreadsheetModel()

        # ----------------------------------------------
        # RECORDER
        # ----------------------------------------------

        self.recorder = SpeechRecorder(
            callback=self.on_transcript
        )

        self.is_recording = False

        # ----------------------------------------------
        # UI
        # ----------------------------------------------

        self.build_ui()
   
    # ==================================================
    # On cell select
    # ==================================================
    def on_cell_select(self, event=None):

        selected = self.sheet.get_currently_selected()

        if not selected:
            return

        self.model.current_row = selected.row
        self.model.current_col = selected.column

    # ==================================================
    # UI
    # ==================================================

    def build_ui(self):

        # ----------------------------------------------
        # MENU
        # ----------------------------------------------

        self.build_menu()

        # ----------------------------------------------
        # TOOLBAR
        # ----------------------------------------------

        toolbar = tk.Frame(self.root)

        toolbar.pack(
            fill=tk.X,
            padx=5,
            pady=5
        )

        # CREATE

        tk.Button(
            toolbar,
            text="Create Spreadsheet",
            command=self.create_spreadsheet
        ).pack(
            side=tk.LEFT,
            padx=2
        )

        # OPEN

        tk.Button(
            toolbar,
            text="Open Spreadsheet",
            command=self.open_spreadsheet
        ).pack(
            side=tk.LEFT,
            padx=2
        )

        # SAVE

        tk.Button(
            toolbar,
            text="Save Spreadsheet",
            command=self.save_spreadsheet
        ).pack(
            side=tk.LEFT,
            padx=2
        )

        # CONDITIONAL FORMATTING

        tk.Button(
            toolbar,
            text="Add Highlight Rule",
            command=self.add_rule
        ).pack(
            side=tk.LEFT,
            padx=2
        )

        # ----------------------------------------------
        # LARGE DICTATION BUTTON
        # ----------------------------------------------

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
            padx=10,
            pady=10
        )

        # ----------------------------------------------
        # STATUS LABEL
        # ----------------------------------------------

        self.status_label = tk.Label(
            self.root,
            text="Ready",
            anchor="w"
        )

        self.status_label.pack(
            fill=tk.X,
            padx=10
        )

        # ----------------------------------------------
        # SPREADSHEET GRID
        # ----------------------------------------------

        self.sheet = Sheet(
            self.root,
            data=[
                ["" for _ in range(26)]
                for _ in range(100)
            ]
        )

        self.sheet.enable_bindings()

        self.sheet.extra_bindings([
            ("cell_select", self.on_cell_select)
        ])

        self.sheet.pack(
            fill=tk.BOTH,
            expand=True,
            padx=5,
            pady=5
        )

        # SELECT FIRST CELL

        self.sheet.select_cell(0, 0)

    # ==================================================
    # MENU
    # ==================================================

    def build_menu(self):

        menubar = tk.Menu(self.root)

        # ----------------------------------------------
        # OPTIONS MENU
        # ----------------------------------------------

        options_menu = tk.Menu(
            menubar,
            tearoff=0
        )

        # MOVEMENT DIRECTION

        self.direction_var = tk.StringVar(
            value="right"
        )

        options_menu.add_radiobutton(
            label="Move Right",
            variable=self.direction_var,
            value="right",
            command=self.set_direction
        )

        options_menu.add_radiobutton(
            label="Move Down",
            variable=self.direction_var,
            value="down",
            command=self.set_direction
        )

        # WRAP OPTION

        self.wrap_var = tk.BooleanVar(
            value=True
        )

        options_menu.add_checkbutton(
            label=(
                "Auto Return to "
                "First Empty Cell"
            ),
            variable=self.wrap_var,
            command=self.set_wrap
        )

        menubar.add_cascade(
            label="Options",
            menu=options_menu
        )

        self.root.config(menu=menubar)

    # ==================================================
    # SETTINGS
    # ==================================================

    def set_direction(self):

        self.model.direction = (
            self.direction_var.get()
        )

        self.status_label.config(
            text=(
                f"Movement direction: "
                f"{self.model.direction}"
            )
        )
        print("Direction:", self.model.direction)

    def set_wrap(self):

        self.model.wrap_enabled = (
            self.wrap_var.get()
        )

        self.status_label.config(
            text=(
                "Auto return: "
                f"{self.model.wrap_enabled}"
            )
        )

    # ==================================================
    # CREATE
    # ==================================================

    def create_spreadsheet(self):

        self.model = SpreadsheetModel()

        self.refresh_sheet()

        self.sheet.select_cell(0, 0)

        self.status_label.config(
            text="New spreadsheet created."
        )

    # ==================================================
    # OPEN
    # ==================================================

    def open_spreadsheet(self):

        path = filedialog.askopenfilename(
            filetypes=[
                (
                    "Spreadsheet Files",
                    "*.xlsx *.ods"
                )
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

            # APPLY HIGHLIGHTS

            for (
                row,
                col
            ), color in formatting.items():

                self.sheet.highlight_cells(
                    row=row,
                    column=col,
                    bg="yellow"
                )

            self.status_label.config(
                text=f"Opened: {path}"
            )

        except Exception as e:

            messagebox.showerror(
                "Open Error",
                str(e)
            )

    # ==================================================
    # SAVE
    # ==================================================

    def save_spreadsheet(self):

        path = filedialog.asksaveasfilename(
            defaultextension=".xlsx",
            filetypes=[
                ("Excel", "*.xlsx")
            ]
        )

        if not path:
            return

        try:

            self.sync_sheet_to_model()

            SpreadsheetIO.save_xlsx(
                self.model,
                path
            )

            self.status_label.config(
                text=f"Saved: {path}"
            )

            messagebox.showinfo(
                "Saved",
                "Spreadsheet saved successfully."
            )

        except Exception as e:

            messagebox.showerror(
                "Save Error",
                str(e)
            )

    # ==================================================
    # RECORDING
    # ==================================================

    def toggle_recording(self):

        if self.is_recording:

            self.recorder.stop()

            self.is_recording = False

            self.dictation_button.config(
                text="START DICTATION",
                bg="green"
            )

            self.status_label.config(
                text="Dictation stopped."
            )

        else:

            self.recorder.start()

            self.is_recording = True

            self.dictation_button.config(
                text="STOP DICTATION",
                bg="red"
            )

            self.status_label.config(
                text="Listening..."
            )

    # ==================================================
    # THREAD SAFE CALLBACK
    # ==================================================

    def on_transcript(self, text):

        self.root.after(
            0,
            lambda: self.process_transcript(text)
        )

    # ==================================================
    # PROCESS TRANSCRIPT
    # ==================================================

    def process_transcript(self, text):

        # ==========================================
        # WRITE TO CURRENT MODEL POSITION
        # ==========================================

        row = self.model.current_row
        col = self.model.current_col

        # ==========================================
        # WRITE CELL
        # ==========================================

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

        # ==========================================
        # MOVE TO NEXT CELL
        # ==========================================

        self.sync_sheet_to_model()
        
        self.model.move_next()

        # ==========================================
        # UPDATE UI SELECTION
        # ==========================================

        self.sheet.select_cell(
            self.model.current_row,
            self.model.current_col
        )

        self.sheet.see(
            self.model.current_row,
            self.model.current_col
        )

        # ==========================================
        # STATUS
        # ==========================================

        self.status_label.config(
            text=(
                f"Entered '{text}' "
                f"at "
                f"({row + 1}, {col + 1})"
            )
        )
    # ==================================================
    # CONDITIONAL FORMATTING
    # ==================================================

    def add_rule(self):

        rule = ConditionalFormattingRule(
            column=0,
            operator=">",
            value=10
        )

        self.model.add_rule(rule)

        self.status_label.config(
            text=(
                "Conditional formatting "
                "rule added."
            )
        )

        messagebox.showinfo(
            "Rule Added",
            "Highlight rule added."
        )

    # ==================================================
    # REFRESH SHEET
    # ==================================================

    def refresh_sheet(self):

        data = (
            self.model.df
            .fillna("")
            .values
            .tolist()
        )

        self.sheet.set_sheet_data(data)

    # ==================================================
    # SYNC TO MODEL
    # ==================================================

    def sync_sheet_to_model(self):

        import pandas as pd

        data = self.sheet.get_sheet_data()

        self.model.df = pd.DataFrame(data)

    # ==================================================
    # CLOSE
    # ==================================================

    def on_close(self):

        try:

            self.recorder.stop()

        except Exception:
            pass

        self.root.destroy()