export default function ItemsList({ items }) {
  return (
    <div>
      <h2 className="font-semibold mb-2">Saved Items</h2>
      <ul className="space-y-1">
        {items.map((item) => (
          <li key={item.id} className="text-sm border p-2">
            <strong>{item.type}</strong>
            <div>{item.preview}</div>
            <div className="text-xs text-gray-500">
              {new Date(item.created_at).toLocaleString()}
            </div>
          </li>
        ))}
      </ul>
    </div>
  );
}
