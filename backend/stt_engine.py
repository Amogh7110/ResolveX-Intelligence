import whisper
import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav


model = whisper.load_model("base")


def listen_audio():

    print("Speak now...")

    duration = 5
    fs = 16000

    recording = sd.rec(
        int(duration * fs),
        samplerate=fs,
        channels=1,
        dtype="int16"
    )

    sd.wait()

    wav.write("input.wav", fs, recording)

    result = model.transcribe("input.wav")

    return result["text"]