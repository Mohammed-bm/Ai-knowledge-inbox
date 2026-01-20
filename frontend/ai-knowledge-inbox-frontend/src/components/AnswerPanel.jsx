export default function AnswerPanel({ answer }) {
  if (!answer) return null;

  return (
    <div className="border p-4 rounded space-y-3">
      <h2 className="font-semibold">Answer</h2>
      <p>{answer.answer}</p>

      {Array.isArray(answer.sources) && answer.sources.length > 0 && (
        <>
          <h3 className="mt-3 text-sm font-semibold">Sources</h3>

          <ul className="text-sm space-y-2">
            {answer.sources.map((s, i) => (
              <li key={i} className="border p-2 rounded">
                <div className="text-xs text-gray-600 mb-1">
                  <strong>Type:</strong> {s.type}{" "}
                  | <strong>Score:</strong> {s.score}
                </div>

                <p>{s.snippet}</p>

                {s.source && (
                  <div className="text-xs text-blue-600 mt-1 break-all">
                    {s.source}
                  </div>
                )}
              </li>
            ))}
          </ul>
        </>
      )}
    </div>
  );
}
