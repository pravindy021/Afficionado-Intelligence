import { useState } from "react";
import { useQuery } from "@tanstack/react-query";
import { getJson } from "../lib/api";

export default function OptimizationPage() {
  const [product, setProduct] = useState("");
  const [change, setChange] = useState(0);
  const [assumption, setAssumption] = useState("baseline");
  const menu = useQuery({ queryKey: ["menu"], queryFn: () => getJson<Record<string, any>>("/optimization/menu") });
  const products = useQuery({
    queryKey: ["products-for-simulator"],
    queryFn: () => getJson<{ products: Array<{ product_detail: string }> }>("/analytics/products"),
  });
  const scenario = useQuery({
    queryKey: ["scenario", product, change, assumption],
    queryFn: () => getJson<Record<string, any>>(`/optimization/pricing?product_detail=${encodeURIComponent(product)}&price_change_percent=${change}&quantity_assumption=${assumption}`),
    enabled: Boolean(product),
  });
  if (menu.isLoading || products.isLoading) return <div className="loading">Loading optimization engine…</div>;
  if (menu.error || products.error) return <div className="error-state">Unable to load optimization data.</div>;
  const names = products.data?.products.map((row) => row.product_detail) ?? [];
  return (
    <div className="page">
      <div className="page-heading"><div><span className="eyebrow">BUSINESS OPTIMIZATION</span><h1>Menu & Pricing</h1></div></div>
      <div className="filters">
        <select value={product} onChange={(event) => setProduct(event.target.value)}><option value="">Select product</option>{names.map((name) => <option key={name} value={name}>{name}</option>)}</select>
        {product && <input type="number" value={change} onChange={(event) => setChange(Number(event.target.value))} aria-label="Hypothetical price change percent" />}
        {product && <select value={assumption} onChange={(event) => setAssumption(event.target.value)}><option value="baseline">Baseline quantity</option><option value="conservative">Conservative +2% lower</option><option value="moderate">Moderate unchanged</option><option value="aggressive">Aggressive +2% higher</option></select>}
      </div>
      {scenario.data && (
        <div className="kpi-grid">
          <article className="kpi-card"><span>Simulated price</span><strong>${scenario.data.simulated_unit_price}</strong></article>
          <article className="kpi-card"><span>Simulated quantity</span><strong>{scenario.data.simulated_quantity}</strong></article>
          <article className="kpi-card"><span>Simulated revenue</span><strong>${scenario.data.simulated_revenue}</strong></article>
          <article className="kpi-card"><span>Revenue difference</span><strong>${scenario.data.revenue_difference}</strong></article>
        </div>
      )}
      {scenario.data && <article className="insights"><span className="eyebrow">HYPOTHESIS NOTICE</span><p>{scenario.data.warning}</p></article>}
      <div className="table-card" style={{ marginTop: 14 }}>
        <table><thead><tr><th>Title</th><th>Evidence</th><th>Recommended action</th><th>Confidence</th><th>Revenue</th></tr></thead>
          <tbody>{menu.data?.recommendations.map((row: any) => <tr key={`${row.title}-${row.supporting_metrics.revenue}`}><td><strong>{row.title}</strong></td><td>{row.business_issue}</td><td>{row.recommended_action}</td><td>{row.confidence}</td><td>${row.supporting_metrics.revenue.toLocaleString()}</td></tr>)}</tbody>
        </table>
      </div>
    </div>
  );
}
