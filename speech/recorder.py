import sounddevice as sd
import numpy as np

SAMPLE_RATE = 16000


def record_audio(seconds=3):

    audio = sd.rec(
        int(seconds * SAMPLE_RATE),
        samplerate=SAMPLE_RATE,
        channels=1,
        dtype='float32'
    )

    sd.wait()

    return np.squeeze(audio)