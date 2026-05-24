import threading
import time


class SpeechRecorder:

    def __init__(self, callback=None):

        self.callback = callback

        self.is_recording = False

    # ==========================================
    # START
    # ==========================================

    def start(self):

        self.is_recording = True

        threading.Thread(
            target=self.loop,
            daemon=True
        ).start()

    # ==========================================
    # STOP
    # ==========================================

    def stop(self):

        self.is_recording = False

    # ==========================================
    # LOOP
    # ==========================================

    def loop(self):

        counter = 1

        while self.is_recording:

            time.sleep(4)

            text = (
                f"Sample {counter}"
            )

            counter += 1

            if self.callback:

                self.callback(text)