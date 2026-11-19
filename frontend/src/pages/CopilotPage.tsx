import { FormEvent, useState } from "react";
import { getJson } from "../lib/api";

export default function CopilotPage() {
  const [question, setQuestion] = useState("");
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<any>(null);
  const suggested = ["Which product generates the most revenue?", "Which category dominates revenue?", "Explain the Pareto distribution.", "Which products contribute the least?"];

  async function ask(event?: FormEvent, proposed?: string) {
    event?.preventDefault();
    const text = proposed ?? question;
    if (!text.trim()) return;
    setLoading(true);
    setResult(null);
    try {
      const response = await fetch("/api/copilot", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ question: text }) });
      if (!response.ok) throw new Error("Copilot request failed");
      setResult(await response.json());
    } catch {
      setResult({ answer: "The grounded Copilot service is currently unavailable.", evidence: [], follow_up_questions: suggested, limitations: ["No unsupported data was substituted."] });
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="page">
      <div className="page-heading"><div><span className="eyebrow">RETRIEVAL-GROUNDED ASSISTANT</span><h1>Afficionado AI Copilot</h1></div></div>
      <div className="suggestions">{suggested.map((item) => <button key={item} onClick={() => ask(undefined, item)}>{item}</button>)}</div>
      <form className="filters" onSubmit={ask}><input value={question} onChange={(event) => setQuestion(event.target.value)} placeholder="Ask a grounded business question" /><button className="icon-button" type="submit" aria-label="Send" disabled={loading}>{loading ? "…" : "→"}</button></form>
      {loading && <div className="loading">Retrieving actual analytics…</div>}
      {result && <article className="insights"><span className="eyebrow">ANSWER</span><p>{result.answer}</p>
        {result.evidence?.length > 0 && <><b>Evidence</b><ul>{result.evidence.map((item: any, index: number) => <li key={index}>{Object.entries(item).map(([key, value]) => `${key}: ${String(value)}`).join(" · ")}</li>)}</ul></>}
        {result.limitations?.map((item: string) => <p key={item}><small>{item}</small></p>)}
        {result.follow_up_questions?.map((item: string) => <button className="follow-up" key={item} onClick={() => ask(undefined, item)}>{item}</button>)}
      </article>}
    </div>
  );
}
