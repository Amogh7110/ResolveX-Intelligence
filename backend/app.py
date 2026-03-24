from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from rag_engine import ask_resolvex
from stt_engine import listen_audio
from tts_engine import speak_audio


app = FastAPI()


# Allow frontend connection
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/ask")
def ask():

    print("🎤 Listening...")

    question = listen_audio()

    if not question:

        return {
            "device": "UNKNOWN DEVICE",
            "solution": "No speech detected.",
            "confidence": 0
        }


    print("Engineer asked:", question)


    result = ask_resolvex(question)

    device = result["device"]
    solution = result["solution"]
    confidence = result["confidence"]


    print("Detected device:", device)
    print("ResolveX solution:", solution)


    # Speak output
    speak_audio(solution)


    return {

        "device": device,
        "solution": solution,
        "confidence": confidence

    }