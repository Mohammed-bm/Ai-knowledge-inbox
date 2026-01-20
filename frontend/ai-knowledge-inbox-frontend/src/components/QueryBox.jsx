import { useState } from "react";
import { queryKnowledge } from "../api";

export default function QueryBox({ onAnswer }) {
  const [question, setQuestion] = useState("");
  const [loading, setLoading] = useState(false);

  async function handleAsk() {
    setLoading(true);
    try {
      const res = await queryKnowledge(question);
      onAnswer(res);
    } catch (err) {
      alert(err.message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="border p-4 rounded">
      <input
        value={question}
        onChange={(e) => setQuestion(e.target.value)}
        placeholder="Ask a question..."
        className="w-full border p-2"
      />
      <button onClick={handleAsk} disabled={loading}>
        Ask
      </button>
    </div>
  );
}
