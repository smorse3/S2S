from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QCheckBox,
    QComboBox,
    QSpinBox,
    QFileDialog
)

from config.settings_manager import SettingsManager


class SettingsDialog(QDialog):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Settings")

        self.settings_manager = SettingsManager()

        self.setup_ui()

    def setup_ui(self):

        layout = QVBoxLayout()

        ##################################################

        self.skip_empty = QCheckBox(
            "Skip Empty Cells"
        )

        layout.addWidget(self.skip_empty)

        ##################################################

        layout.addWidget(
            QLabel("Delay after speech (ms)")
        )

        self.delay_spin = QSpinBox()

        self.delay_spin.setRange(100, 10000)

        self.delay_spin.setValue(1500)

        layout.addWidget(self.delay_spin)

        ##################################################

        layout.addWidget(
            QLabel("Movement Direction")
        )

        self.direction_combo = QComboBox()

        self.direction_combo.addItems([
            "right",
            "left",
            "up",
            "down"
        ])

        layout.addWidget(self.direction_combo)

        ##################################################

        save_btn = QPushButton("Save Settings")

        load_btn = QPushButton("Load Settings")

        layout.addWidget(save_btn)

        layout.addWidget(load_btn)

        ##################################################

        save_btn.clicked.connect(self.save_settings)

        load_btn.clicked.connect(self.load_settings)

        ##################################################

        self.setLayout(layout)

    def save_settings(self):

        path, _ = QFileDialog.getSaveFileName(
            self,
            "Save Settings",
            "",
            "YAML (*.yaml)"
        )

        if not path:
            return

        settings = {
            "skip_empty": self.skip_empty.isChecked(),
            "delay": self.delay_spin.value(),
            "direction": self.direction_combo.currentText()
        }

        self.settings_manager.save(
            path,
            settings
        )

    def load_settings(self):

        path, _ = QFileDialog.getOpenFileName(
            self,
            "Load Settings",
            "",
            "YAML (*.yaml)"
        )

        if not path:
            return

        settings = self.settings_manager.load(path)

        self.skip_empty.setChecked(
            settings.get("skip_empty", False)
        )

        self.delay_spin.setValue(
            settings.get("delay", 1500)
        )