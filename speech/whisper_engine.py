from faster_whisper import WhisperModel

model = WhisperModel(
    "base",
    device="cpu",
    compute_type="int8"
)


def transcribe(audio):

    segments, info = model.transcribe(
        audio,
        vad_filter=True
    )

    text = " ".join(
        seg.text for seg in segments
    )

    return text.strip()