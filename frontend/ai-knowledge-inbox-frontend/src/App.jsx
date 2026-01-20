import { useEffect, useState } from "react";
import { fetchItems } from "./api";
import IngestForm from "./components/IngestForm";
import ItemsList from "./components/ItemsList";
import QueryBox from "./components/QueryBox";
import AnswerPanel from "./components/AnswerPanel";

export default function App() {
  const [items, setItems] = useState([]);
  const [answer, setAnswer] = useState(null);
  const [error, setError] = useState(null);

  async function loadItems() {
    try {
      const data = await fetchItems();
      setItems(data);
    } catch (err) {
      setError(err.message);
    }
  }

  useEffect(() => {
    loadItems();
  }, []);

  return (
    <div className="max-w-3xl mx-auto p-4 space-y-6">
      <h1 className="text-2xl font-bold">AI Knowledge Inbox</h1>

      <IngestForm onSuccess={loadItems} />
      <ItemsList items={items} />
      <QueryBox onAnswer={setAnswer} />
      <AnswerPanel answer={answer} />

      {error && <p className="text-red-500">{error}</p>}
    </div>
  );
}
