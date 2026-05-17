from PySide6.QtCore import QThread, Signal

from speech.recorder import record_audio

from speech.whisper_engine import transcribe


class DictationThread(QThread):

    text_ready = Signal(str)

    def __init__(self):
        super().__init__()

        self.running = True

    def run(self):

        while self.running:

            audio = record_audio(3)

            text = transcribe(audio)

            if text:
                self.text_ready.emit(text)

    def stop(self):

        self.running = False