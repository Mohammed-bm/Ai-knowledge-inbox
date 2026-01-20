const API_BASE = "http://localhost:8000";

export async function ingestContent(payload) {
  const res = await fetch(`${API_BASE}/ingest/`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });

  if (!res.ok) {
    throw new Error("Failed to ingest content");
  }

  return res.json();
}

export async function fetchItems() {
  const res = await fetch(`${API_BASE}/items/`);
  if (!res.ok) throw new Error("Failed to fetch items");
  return res.json();
}

export async function queryKnowledge(question) {
  const res = await fetch(`${API_BASE}/query/`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ question }),
  });

  if (!res.ok) throw new Error("Query failed");
  return res.json();
}
