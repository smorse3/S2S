import tkinter as tk

from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox

from datetime import datetime

from speech.recorder import SpeechRecorder
from spreadsheet.pandas_handler import (
    PandasSpreadsheetHandler
)


class MainWindow:

    def __init__(self, root):

        self.root = root

        self.root.title(
            "Speech to Spreadsheet"
        )

        self.root.geometry("900x600")

        # =========================
        # STATE
        # =========================

        self.is_recording = False

        # =========================
        # SPREADSHEET ENGINE
        # =========================

        self.spreadsheet = (
            PandasSpreadsheetHandler()
        )

        self.spreadsheet.set_columns([
            "Timestamp",
            "Speaker",
            "Transcript"
        ])

        # =========================
        # SPEECH RECORDER
        # =========================

        self.recorder = SpeechRecorder(
            callback=self.on_transcript
        )

        # =========================
        # UI
        # =========================

        self.build_ui()

    # ==================================================
    # UI SETUP
    # ==================================================

    def build_ui(self):

        # --------------------------
        # TITLE
        # --------------------------

        title_label = tk.Label(
            self.root,
            text="Speech to Spreadsheet",
            font=("Arial", 18, "bold")
        )

        title_label.pack(
            pady=10
        )

        # --------------------------
        # BUTTON FRAME
        # --------------------------

        button_frame = tk.Frame(
            self.root
        )

        button_frame.pack(
            pady=10
        )

        # --------------------------
        # START BUTTON
        # --------------------------

        self.start_button = tk.Button(
            button_frame,
            text="Start Recording",
            width=18,
            command=self.start_recording
        )

        self.start_button.grid(
            row=0,
            column=0,
            padx=5
        )

        # --------------------------
        # STOP BUTTON
        # --------------------------

        self.stop_button = tk.Button(
            button_frame,
            text="Stop Recording",
            width=18,
            command=self.stop_recording,
            state=tk.DISABLED
        )

        self.stop_button.grid(
            row=0,
            column=1,
            padx=5
        )

        # --------------------------
        # EXPORT BUTTON
        # --------------------------

        self.export_button = tk.Button(
            button_frame,
            text="Export Spreadsheet",
            width=18,
            command=self.export_spreadsheet
        )

        self.export_button.grid(
            row=0,
            column=2,
            padx=5
        )

        # --------------------------
        # STATUS LABEL
        # --------------------------

        self.status_label = tk.Label(
            self.root,
            text="Ready",
            fg="green",
            font=("Arial", 10, "bold")
        )

        self.status_label.pack(
            pady=5
        )

        # --------------------------
        # TRANSCRIPT TABLE
        # --------------------------

        self.tree = ttk.Treeview(
            self.root,
            columns=(
                "Timestamp",
                "Speaker",
                "Transcript"
            ),
            show="headings"
        )

        self.tree.heading(
            "Timestamp",
            text="Timestamp"
        )

        self.tree.heading(
            "Speaker",
            text="Speaker"
        )

        self.tree.heading(
            "Transcript",
            text="Transcript"
        )

        self.tree.column(
            "Timestamp",
            width=180
        )

        self.tree.column(
            "Speaker",
            width=100
        )

        self.tree.column(
            "Transcript",
            width=550
        )

        self.tree.pack(
            fill=tk.BOTH,
            expand=True,
            padx=10,
            pady=10
        )

        # --------------------------
        # SCROLLBAR
        # --------------------------

        scrollbar = ttk.Scrollbar(
            self.tree,
            orient="vertical",
            command=self.tree.yview
        )

        self.tree.configure(
            yscrollcommand=scrollbar.set
        )

        scrollbar.pack(
            side="right",
            fill="y"
        )

    # ==================================================
    # RECORDING CONTROL
    # ==================================================

    def start_recording(self):

        if self.is_recording:
            return

        try:

            self.recorder.start()

            self.is_recording = True

            self.status_label.config(
                text="Recording...",
                fg="red"
            )

            self.start_button.config(
                state=tk.DISABLED
            )

            self.stop_button.config(
                state=tk.NORMAL
            )

        except Exception as e:

            messagebox.showerror(
                "Recording Error",
                str(e)
            )

    def stop_recording(self):

        if not self.is_recording:
            return

        try:

            self.recorder.stop()

            self.is_recording = False

            self.status_label.config(
                text="Stopped",
                fg="green"
            )

            self.start_button.config(
                state=tk.NORMAL
            )

            self.stop_button.config(
                state=tk.DISABLED
            )

        except Exception as e:

            messagebox.showerror(
                "Stop Error",
                str(e)
            )

    # ==================================================
    # TRANSCRIPT CALLBACK
    # ==================================================

    def on_transcript(self, transcript):

        transcript = transcript.strip()

        if not transcript:
            return

        timestamp = datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )

        speaker = "User"

        # --------------------------
        # SAVE TO DATAFRAME
        # --------------------------

        self.spreadsheet.append_row([
            timestamp,
            speaker,
            transcript
        ])

        # --------------------------
        # UPDATE TABLE
        # --------------------------

        self.tree.insert(
            "",
            tk.END,
            values=(
                timestamp,
                speaker,
                transcript
            )
        )

        # Auto-scroll

        self.tree.yview_moveto(1)

    # ==================================================
    # EXPORT
    # ==================================================

    def export_spreadsheet(self):

        if not self.spreadsheet.rows:

            messagebox.showwarning(
                "No Data",
                "No transcript data available."
            )

            return

        file_path = (
            filedialog.asksaveasfilename(
                defaultextension=".xlsx",
                filetypes=[
                    (
                        "Excel Files",
                        "*.xlsx"
                    ),
                    (
                        "CSV Files",
                        "*.csv"
                    )
                ]
            )
        )

        if not file_path:
            return

        try:

            if file_path.endswith(".csv"):

                self.spreadsheet.save_csv(
                    file_path
                )

            else:

                self.spreadsheet.save_xlsx(
                    file_path
                )

            messagebox.showinfo(
                "Export Complete",
                (
                    "Spreadsheet exported "
                    "successfully."
                )
            )

        except Exception as e:

            messagebox.showerror(
                "Export Error",
                str(e)
            )

    # ==================================================
    # CLEANUP
    # ==================================================

    def on_close(self):

        try:

            if self.is_recording:

                self.recorder.stop()

        except Exception:
            pass

        self.root.destroy()