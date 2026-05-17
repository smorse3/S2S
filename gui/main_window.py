from PySide6.QtCore import Qt

from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
    QHBoxLayout,
    QFileDialog,
    QMessageBox,
    QLabel
)

from gui.settings_dialog import SettingsDialog
from gui.term_dialog import TermDialog

from spreadsheet.libreoffice_handler import LibreOfficeHandler

from speech.dictation_thread import DictationThread


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Speech Spreadsheet")

        self.resize(1200, 700)

        ###################################################
        # LIBREOFFICE HANDLER
        ###################################################

        self.spreadsheet = LibreOfficeHandler()

        try:

            self.spreadsheet.connect()

        except Exception as e:

            QMessageBox.critical(
                self,
                "LibreOffice Connection Error",
                (
                    "Could not connect to LibreOffice.\n\n"
                    "Make sure LibreOffice is running in UNO mode.\n\n"
                    f"Error:\n{e}"
                )
            )

        ###################################################
        # DICTATION THREAD
        ###################################################

        self.dictation_thread = None

        ###################################################
        # UI
        ###################################################

        self.setup_ui()

    ###################################################
    # UI SETUP
    ###################################################

    def setup_ui(self):

        central = QWidget()

        self.setCentralWidget(central)

        root = QHBoxLayout()

        central.setLayout(root)

        ###################################################
        # LEFT PANEL
        ###################################################

        left_panel = QVBoxLayout()

        self.create_btn = QPushButton(
            "Create Spreadsheet"
        )

        self.open_btn = QPushButton(
            "Open Spreadsheet"
        )

        self.save_btn = QPushButton(
            "Save Spreadsheet"
        )

        self.dictation_btn = QPushButton(
            "Dictation Start"
        )

        self.term_btn = QPushButton(
            "Term Recognition"
        )

        self.settings_btn = QPushButton(
            "Settings"
        )

        buttons = [
            self.create_btn,
            self.open_btn,
            self.save_btn,
            self.dictation_btn,
            self.term_btn,
            self.settings_btn
        ]

        for b in buttons:

            b.setMinimumHeight(45)

            left_panel.addWidget(b)

        left_panel.addStretch()

        ###################################################
        # LARGE START / STOP BUTTON
        ###################################################

        self.big_button = QPushButton("START")

        self.big_button.setFixedSize(180, 180)

        self.big_button.setStyleSheet("""
        QPushButton {
            border-radius: 90px;
            background-color: #C0C0C0;
            border: 3px outset gray;
            font-size: 22px;
            font-weight: bold;
        }

        QPushButton:pressed {
            border: 3px inset gray;
        }
        """)

        left_panel.addWidget(
            self.big_button,
            alignment=Qt.AlignCenter
        )

        root.addLayout(left_panel, 1)

        ###################################################
        # RIGHT PANEL
        ###################################################

        right_panel = QVBoxLayout()

        ###################################################
        # INSTRUCTIONS
        ###################################################

        self.instructions = QTextEdit()

        self.instructions.setReadOnly(True)

        self.instructions.setText(
            "You can start in four quick steps:\n\n"
            "1. Create or open spreadsheet\n"
            "2. Select starting location\n"
            "3. Press Dictation\n"
            "4. Speak your text\n"
        )

        right_panel.addWidget(self.instructions)

        ###################################################
        # CURRENT POSITION
        ###################################################

        self.position_label = QLabel(
            "Current Cell: A1"
        )

        self.position_label.setStyleSheet("""
        font-size: 18px;
        font-weight: bold;
        """)

        right_panel.addWidget(
            self.position_label
        )

        ###################################################
        # MOVEMENT BUTTONS
        ###################################################

        self.right_btn = QPushButton(
            "Move Right"
        )

        self.left_btn = QPushButton(
            "Move Left"
        )

        self.up_btn = QPushButton(
            "Move Up"
        )

        self.down_btn = QPushButton(
            "Move Down"
        )

        right_panel.addWidget(self.right_btn)
        right_panel.addWidget(self.left_btn)
        right_panel.addWidget(self.up_btn)
        right_panel.addWidget(self.down_btn)

        root.addLayout(right_panel, 4)

        ###################################################
        # SIGNALS
        ###################################################

        self.create_btn.clicked.connect(
            self.create_spreadsheet
        )

        self.open_btn.clicked.connect(
            self.open_spreadsheet
        )

        self.save_btn.clicked.connect(
            self.save_spreadsheet
        )

        self.settings_btn.clicked.connect(
            self.open_settings
        )

        self.term_btn.clicked.connect(
            self.open_terms
        )

        self.dictation_btn.clicked.connect(
            self.toggle_dictation
        )

        self.big_button.clicked.connect(
            self.toggle_dictation
        )

        self.right_btn.clicked.connect(
            selfmove_right
        )

        self.left_btn.clicked.connect(
            self.move_left
        )

        self.up_btn.clicked.connect(
            self.move_up
        )

        self.down_btn.clicked.connect(
            self.move_down
        )

    ###################################################
    # SPREADSHEET FUNCTIONS
    ###################################################

    def create_spreadsheet(self):

        self.spreadsheet.create_document()

        self.update_position()

        QMessageBox.information(
            self,
            "Spreadsheet",
            "New LibreOffice spreadsheet created."
        )

    def open_spreadsheet(self):

        path, _ = QFileDialog.getOpenFileName(
            self,
            "Open Spreadsheet",
            "",
            "Spreadsheet (*.ods *.xlsx)"
        )

        if not path:
            return

        self.spreadsheet.open_document(path)

        self.update_position()

        QMessageBox.information(
            self,
            "Spreadsheet",
            "Spreadsheet opened."
        )

    def save_spreadsheet(self):

        self.spreadsheet.save()

        QMessageBox.information(
            self,
            "Spreadsheet",
            "Spreadsheet saved."
        )

    ###################################################
    # SETTINGS
    ###################################################

    def open_settings(self):

        dialog = SettingsDialog(self)

        dialog.exec()

    ###################################################
    # TERM RECOGNITION
    ###################################################

    def open_terms(self):

        dialog = TermDialog(self)

        dialog.exec()

    ###################################################
    # DICTATION
    ###################################################

    def toggle_dictation(self):

        if self.dictation_thread is None:

            self.start_dictation()

        else:

            self.stop_dictation()

    def start_dictation(self):

        self.dictation_thread = DictationThread()

        self.dictation_thread.text_ready.connect(
            self.handle_transcription
        )

        self.dictation_thread.start()

        self.big_button.setText("STOP")

    def stop_dictation(self):

        if self.dictation_thread:

            self.dictation_thread.stop()

            self.dictation_thread.wait()

            self.dictation_thread = None

        self.big_button.setText("START")

    ###################################################
    # TRANSCRIPTION HANDLING
    ###################################################

    def handle_transcription(self, text):

        print("Recognized:", text)

        self.spreadsheet.write_current_cell(text)

        self.spreadsheet.move_next()

        self.update_position()

    ###################################################
    # MOVEMENT
    ###################################################

    def move_right(self):

        self.spreadsheet.move_right()

        self.update_position()

    def move_left(self):

        self.spreadsheet.move_left()

        self.update_position()

    def move_up(self):

        self.spreadsheet.move_up()

        self.update_position()

    def move_down(self):

        self.spreadsheet.move_down()

        self.update_position()

    ###################################################
    # POSITION DISPLAY
    ###################################################

    def update_position(self):

        position = self.spreadsheet.get_position_string()

        self.position_label.setText(
            f"Current Cell: {position}"
        )