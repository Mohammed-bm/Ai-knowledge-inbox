import { useState } from "react";
import { ingestContent } from "../api";

export default function IngestForm({ onSuccess }) {
  const [type, setType] = useState("note");
  const [content, setContent] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  async function handleSubmit(e) {
    e.preventDefault();
    if (!content.trim()) return;

    try {
      setLoading(true);
      setError(null);

      // 🔴 THIS WAS THE BUG
      const payload =
        type === "note"
          ? { type: "note", raw_text: content }
          : { type: "url", source: content };

      await ingestContent(payload);

      setContent("");
      onSuccess?.();
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <form onSubmit={handleSubmit} className="border p-4 rounded space-y-3">
      <h2 className="font-semibold">Add Content</h2>

      <select
        value={type}
        onChange={(e) => setType(e.target.value)}
        className="border p-2 w-full"
      >
        <option value="note">Note</option>
        <option value="url">URL</option>
      </select>

      {type === "note" ? (
        <textarea
          placeholder="Write a short note…"
          value={content}
          onChange={(e) => setContent(e.target.value)}
          className="w-full border p-2"
          rows={4}
        />
      ) : (
        <input
          placeholder="https://example.com"
          value={content}
          onChange={(e) => setContent(e.target.value)}
          className="w-full border p-2"
        />
      )}

      <button type="submit" disabled={loading} className="border px-3 py-1">
        {loading ? "Saving..." : "Save"}
      </button>

      {error && <p className="text-red-500 text-sm">{error}</p>}
    </form>
  );
}
