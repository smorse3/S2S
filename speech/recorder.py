import threading

import speech_recognition as sr


class SpeechRecorder:

    def __init__(self, callback=None):

        self.callback = callback

        self.is_recording = False

        self.recognizer = sr.Recognizer()

    def start(self):

        self.is_recording = True

        threading.Thread(
            target=self.loop,
            daemon=True
        ).start()

    def stop(self):

        self.is_recording = False

    def loop(self):

        with sr.Microphone() as source:

            while self.is_recording:

                try:

                    audio = (
                        self.recognizer.listen(
                            source
                        )
                    )

                    text = (
                        self.recognizer
                        .recognize_google(audio)
                    )

                    if self.callback:

                        self.callback(text)

                except Exception as e:

                    print(e)