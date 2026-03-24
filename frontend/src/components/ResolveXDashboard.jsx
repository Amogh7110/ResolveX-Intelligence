import { useState } from "react";
import axios from "axios";
import logo from "../assets/resolvex-logo.png";

export default function ResolveXDashboard() {

  const [deviceName, setDeviceName] = useState("DEVICE NOT DETECTED");
  const [responseText, setResponseText] = useState("");
  const [displayText, setDisplayText] = useState("");
  const [confidence, setConfidence] = useState(0);
  const [loading, setLoading] = useState(false);


  // =============================
  // TYPEWRITER STREAM EFFECT
  // =============================

  const streamResponse = (text) => {

    let index = 0;

    setDisplayText("");

    const interval = setInterval(() => {

      setDisplayText(prev => prev + text[index]);

      index++;

      if (index >= text.length)
        clearInterval(interval);

    }, 12);
  };


  // =============================
  // TEXT TO SPEECH ENGINE
  // =============================

  const speak = (text) => {

    const speech = new SpeechSynthesisUtterance(text);

    speech.rate = 1;
    speech.pitch = 1;
    speech.volume = 1;

    window.speechSynthesis.cancel();
    window.speechSynthesis.speak(speech);

  };


  // =============================
  // MAIN RESOLVEX QUERY FUNCTION
  // =============================

  const askResolveX = async () => {

    setLoading(true);

    try {

      const res = await axios.get(
        "http://127.0.0.1:8000/ask"
      );

      const solution = res.data.solution;
      const confidenceValue = res.data.confidence;
      const detectedDevice = res.data.device;

      setDeviceName(detectedDevice);
      setResponseText(solution);
      setConfidence(confidenceValue);

      streamResponse(solution);

      speak(solution);

    }

    catch {

      alert("ResolveX backend not responding");

    }

    setLoading(false);

  };


  return (

    <div className="dashboard">


      {/* HEADER */}

      <header>

        <div className="logo-container">

          <img
            src={logo}
            width="55"
          />

          <h1>ResolveX Intelligence</h1>

        </div>

        <span className="engineer-mode">

          ENGINEER MODE ACTIVE

        </span>

      </header>



      {/* MAIN GRID */}

      <div className="main-panel">


        {/* DEVICE PANEL */}

        <div className="device-box">

          <h2>{deviceName}</h2>

          <div className="error-line">

            {loading
              ? "Analyzing device fault..."
              : "Awaiting diagnosis..."}

          </div>

        </div>



        {/* VOICE CORE */}

        <div className="voice-core">

          <button
            onClick={askResolveX}
            className="mic-button"
          >

            🎤

          </button>


          <p>

            {loading
              ? "ResolveX listening engineer..."
              : "Awaiting biomedical engineer command"}

          </p>

        </div>



        {/* CONFIDENCE PANEL */}

        <div className="confidence-circle">

          {confidence}%

          <br />

          CONFIDENCE

        </div>

      </div>



      {/* RESPONSE STREAM */}

      <div className="response-stream">

        <h3>

          AI RESPONSE STREAM

        </h3>


        <pre>

          {displayText}

        </pre>

      </div>



      {/* FOOTER */}

      <footer>

        VOICE ONLINE |
        VECTOR MEMORY ACTIVE |
        RAG ENGINE CONNECTED |
        BIOMEDICAL AI READY

      </footer>


    </div>

  );

}