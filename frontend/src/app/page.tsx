"use client";

import { useState } from "react";

export default function Home() {
  const [text, setText] = useState("");
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<{
    label: string;
    score: number;
    all_scores: Record<string, number>;
    processed_text?: string;
  } | null>(null);

  const predefinedExamples = [
    { text: "I am soooo hapy right now!", label: "Joy" },
    { text: "This is deeply tragic and breaks my heart.", label: "Sadness" },
    { text: "I am absolutely furious about what happened today!", label: "Anger" },
    { text: "I am terrified of the dark and what might be in it.", label: "Fear" },
    { text: "I adore spending time with my lovely family.", label: "Love" },
    { text: "I am completely shocked by this sudden news!!!", label: "Surprise" },
  ];

  const handlePredict = async (inputText: string = text) => {
    if (!inputText.trim()) return;

    setLoading(true);
    setResult(null);
    try {
      const response = await fetch("http://localhost:8000/predict", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ text: inputText }),
      });

      if (!response.ok) throw new Error("API failed");
      const data = await response.json();
      setResult(data);
    } catch (error) {
      console.error(error);
      alert("Failed to connect to the backend. Is FastAPI running?");
    } finally {
      setLoading(false);
    }
  };

  const getEmotionColor = (emotion: string) => {
    return `var(--color-${emotion})`;
  };

  return (
    <main className="container">
      <div style={{ textAlign: "center", marginBottom: "40px" }}>
        <h1>Emotion Flow</h1>
        <p className="subtitle">Emotion Flow: Real-time Emotion Intelligence Dashboard</p>
      </div>

      <div className="grid-layout">
        <div className="glass-panel">
          <h2>Input Text</h2>
          <textarea
            placeholder="Type or paste your text here (Try adding typos like 'sooo hapy')..."
            value={text}
            onChange={(e) => setText(e.target.value)}
          />
          <button
            className="primary-btn"
            onClick={() => handlePredict(text)}
            disabled={loading || text.trim() === ""}
          >
            {loading ? <div className="loader"></div> : "Analyze Emotion"}
          </button>

          <div style={{ marginTop: "24px" }}>
            <h3 style={{ fontSize: "0.875rem", color: "var(--text-secondary)", marginBottom: "8px" }}>Try an example for each emotion:</h3>
            <div style={{ display: "flex", flexDirection: "column", gap: "8px" }}>
              {predefinedExamples.map((ex, i) => (
                <button
                  key={i}
                  style={{
                    padding: "8px 12px",
                    textAlign: "left",
                    backgroundColor: "transparent",
                    border: "1px solid var(--border-color)",
                    borderRadius: "6px",
                    cursor: "pointer",
                    fontSize: "0.875rem",
                    transition: "border-color 0.2s",
                    display: "flex",
                    justifyContent: "space-between"
                  }}
                  onMouseOver={(e) => e.currentTarget.style.borderColor = "var(--accent-color)"}
                  onMouseOut={(e) => e.currentTarget.style.borderColor = "var(--border-color)"}
                  onClick={() => {
                    setText(ex.text);
                    handlePredict(ex.text);
                  }}
                >
                  <span style={{ fontStyle: "italic" }}>"{ex.text}"</span>
                  <span style={{ fontSize: "0.75rem", color: "var(--text-secondary)", fontWeight: 600 }}>{ex.label}</span>
                </button>
              ))}
            </div>
          </div>
        </div>

        <div className="glass-panel">
          <h2>Analysis Results</h2>
          {loading ? (
            <div style={{ display: "flex", justifyContent: "center", alignItems: "center", height: "200px", color: "var(--text-secondary)" }}>
              Analyzing text...
            </div>
          ) : result ? (
            <>
              {result.processed_text &&
                result.processed_text.replace(/\s+/g, ' ').trim() !== text.toLowerCase().replace(/\s+/g, ' ').trim() && (
                  <div style={{
                    backgroundColor: "rgba(59, 130, 246, 0.1)",
                    padding: "12px",
                    borderRadius: "8px",
                    fontSize: "0.875rem",
                    marginBottom: "16px",
                    borderLeft: "4px solid var(--accent-color)"
                  }}>
                    <div style={{ fontWeight: 700, color: "var(--accent-color)", marginBottom: "4px" }}>
                      ✨ Typo Correction & Normalization Applied
                    </div>
                    <span style={{ color: "var(--text-secondary)" }}>Engineered input: </span>
                    <span style={{ fontStyle: "italic" }}>"{result.processed_text}"</span>
                  </div>
                )}

              <div className="result-card">
                <div
                  className="emotion-label"
                  style={{ color: getEmotionColor(result.label) }}
                >
                  {result.label}
                </div>
                <div className="emotion-score">
                  Confidence: {(result.score * 100).toFixed(1)}%
                </div>
              </div>

              <div className="bars-container">
                <h3 style={{ fontSize: "1rem", marginBottom: "16px" }}>Detailed Distribution</h3>
                {Object.entries(result.all_scores)
                  .sort(([, a], [, b]) => b - a)
                  .map(([emotion, score]) => (
                    <div className="bar-row" key={emotion}>
                      <div className="bar-label">{emotion}</div>
                      <div className="bar-track">
                        <div
                          className="bar-fill"
                          style={{
                            width: `${score * 100}%`,
                            backgroundColor: getEmotionColor(emotion)
                          }}
                        ></div>
                      </div>
                      <div className="bar-value">{(score * 100).toFixed(1)}%</div>
                    </div>
                  ))}
              </div>
            </>
          ) : (
            <div style={{ display: "flex", justifyContent: "center", alignItems: "center", height: "200px", color: "var(--text-secondary)", textAlign: "center" }}>
              Awaiting input...<br />Results will appear here.
            </div>
          )}
        </div>
      </div>
    </main>
  );
}
