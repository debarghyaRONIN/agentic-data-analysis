import { useState, useRef, useEffect } from "react";
import axios from "axios";
import { uploadDataset } from "../api";
import ChatCharts from "./ChatCharts";

const API_URL = "http://127.0.0.1:8000";

export default function Chat() {
  const [messages, setMessages] = useState([
    {
      sender: "agent",
      type: "text",
      text:
        "Hello 👋 Upload a dataset using the 📎 icon and then chat with me about your business data."
    }
  ]);

  const [input, setInput] = useState("");
  const [isThinking, setIsThinking] = useState(false);
  const [datasetUploaded, setDatasetUploaded] = useState(false);

  const fileInputRef = useRef(null);
  const chatBoxRef = useRef(null);

  const suggestedQuestions = [
    "What is happening with my business?",
    "Show me the demand trend",
    "How strong is customer demand?",
    "Should I increase inventory?",
    "Explain the decision in simple terms"
  ];


  // AUTO SCROLL
  useEffect(() => {
    chatBoxRef.current?.scrollTo({
      top: chatBoxRef.current.scrollHeight,
      behavior: "smooth"
    });
  }, [messages]);


  // SEND MESSAGE (ONLY AFTER UPLOAD)

  const sendMessage = async (text) => {
    if (!text.trim() || isThinking) return;

    if (!datasetUploaded) return;

    setInput("");

    setMessages(prev => [
      ...prev,
      { sender: "user", type: "text", text }
    ]);

    setMessages(prev => [
      ...prev,
      { sender: "agent", type: "thinking", thinking: true }
    ]);

    setIsThinking(true);

    try {
      const res = await axios.post(`${API_URL}/chat`, {
        message: text
      });

      setMessages(prev =>
        prev.map(msg =>
          msg.thinking
            ? {
                sender: "agent",
                type: "text",
                text: res.data.reply
              }
            : msg
        )
      );
    } catch {
      setMessages(prev =>
        prev.map(msg =>
          msg.thinking
            ? {
                sender: "agent",
                type: "text",
                text: "❌ Something went wrong while analyzing your data."
              }
            : msg
        )
      );
    } finally {
      setIsThinking(false);
    }
  };

  // FILE UPLOAD → AGENT CHART MESSAGE

  const handleFileUpload = async (e) => {
  const file = e.target.files[0];
  if (!file) return;

  setDatasetUploaded(false);

  setMessages(prev => [
    ...prev,
    {
      sender: "user",
      type: "text",
      text: `📎 Uploaded dataset: ${file.name}`
    }
  ]);

  try {
    await uploadDataset(file);

    setMessages(prev => [
      ...prev,
      {
        sender: "agent",
        type: "text",
        text:
          "✅ Dataset uploaded successfully! Generating insights and charts…"
      }
    ]);

    setMessages(prev => [
      ...prev,
      {
        sender: "agent",
        type: "thinking",
        thinking: true
      }
    ]);

    const res = await axios.post(`${API_URL}/chat`, {
      message: "Show me the overall trends"
    });

    setMessages(prev =>
      prev.map(msg =>
        msg.thinking
          ? {
              sender: "agent",
              type: "charts",
              charts: res.data.charts
            }
          : msg
      )
    );

    setDatasetUploaded(true);
  } catch {
    setMessages(prev =>
      prev.map(msg =>
        msg.thinking
          ? {
              sender: "agent",
              type: "text",
              text: "❌ Failed to analyze the dataset. Please try again."
            }
          : msg
      )
    );
  }

  e.target.value = null;
};

  return (
    <div className="chat-container">
      {/* CHAT */}
      <div className="chat-box" ref={chatBoxRef}>
        {messages.map((msg, i) => (
          <div
            key={i}
            className={`chat-message ${msg.sender} ${
              msg.thinking ? "thinking" : "animate-in"
            }`}
          >
            {msg.thinking && (
              <div className="skeleton">
                <div className="skeleton-line short" />
                <div className="skeleton-line" />
                <div className="skeleton-line medium" />
              </div>
            )}

            {!msg.thinking && msg.type === "text" && msg.text}

            {!msg.thinking && msg.type === "charts" && (
              <ChatCharts data={msg.charts} />
            )}
          </div>
        ))}
      </div>

      {/*  SUGGESTIONS  */}
      <div className="suggestions">
        {suggestedQuestions.map((q, i) => (
          <button
            key={i}
            className="suggestion-chip"
            disabled={isThinking || !datasetUploaded}
            onClick={() => sendMessage(q)}
          >
            {q}
          </button>
        ))}
      </div>

      {/* INPUT */}
      <div className="chat-input">
        <button
          className="attach-btn"
          onClick={() => fileInputRef.current.click()}
          disabled={isThinking}
        >
          📎
        </button>

        <input
          type="file"
          accept=".csv"
          ref={fileInputRef}
          style={{ display: "none" }}
          onChange={handleFileUpload}
        />

        <input
          type="text"
          placeholder={
            datasetUploaded
              ? isThinking
                ? "Agent is thinking…"
                : "Ask about trends, demand, or decisions…"
              : "Upload a dataset to begin…"
          }
          value={input}
          disabled={isThinking || !datasetUploaded}
          onChange={e => setInput(e.target.value)}
          onKeyDown={e =>
            e.key === "Enter" && sendMessage(input)
          }
        />

        <button
          className="send-btn"
          onClick={() => sendMessage(input)}
          disabled={isThinking || !datasetUploaded}
        >
          ➤
        </button>
      </div>
    </div>
  );
}