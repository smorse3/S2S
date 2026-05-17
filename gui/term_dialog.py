from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QPushButton,
    QTableWidget,
    QTableWidgetItem
)


class TermDialog(QDialog):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Term Recognition")

        self.setup_ui()

    def setup_ui(self):

        layout = QVBoxLayout()

        self.table = QTableWidget(20, 2)

        self.table.setHorizontalHeaderLabels([
            "Spoken",
            "Replacement"
        ])

        layout.addWidget(self.table)

        self.save_btn = QPushButton("Save")

        layout.addWidget(self.save_btn)

        self.setLayout(layout)