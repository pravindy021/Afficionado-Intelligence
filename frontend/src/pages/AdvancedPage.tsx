import { useQuery } from "@tanstack/react-query";
import { ScatterChart, Scatter, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, BarChart, Bar } from "recharts";
import { getJson } from "../lib/api";

type Mode = "segmentation" | "clustering" | "anomalies" | "statistics";

const titles: Record<Mode, { title: string; eyebrow: string }> = {
  segmentation: { title: "Product Segmentation", eyebrow: "EXPLAINABLE PORTFOLIO SEGMENTS" },
  clustering: { title: "Product Clustering", eyebrow: "SCALED K-MEANS ANALYSIS" },
  anomalies: { title: "Anomaly Detection", eyebrow: "STATISTICAL OUTLIER REVIEW" },
  statistics: { title: "Statistical Intelligence", eyebrow: "DESCRIPTIVE ANALYSIS" },
};

export default function AdvancedPage({ mode }: { mode: Mode }) {
  const endpoint = `/analytics/${mode === "statistics" ? "statistics" : mode === "segmentation" ? "segmentation" : mode}`;
  const { data, isLoading, error } = useQuery({ queryKey: [mode], queryFn: () => getJson<Record<string, any>>(endpoint) });
  if (isLoading) return <div className="loading">Loading {titles[mode].title.toLowerCase()}…</div>;
  if (error) return <div className="error-state">Unable to load {titles[mode].title.toLowerCase()}.</div>;
  if (!data) return null;

  return (
    <div className="page">
      <div className="page-heading"><div><span className="eyebrow">{titles[mode].eyebrow}</span><h1>{titles[mode].title}</h1></div></div>
      {mode === "segmentation" && (
        <>
          <div className="kpi-grid">
            {data.summary?.map((row: any) => <article className="kpi-card" key={row.segment}><span>{row.segment}</span><strong>{row.products}</strong><small>{row.revenue.toLocaleString(undefined, { maximumFractionDigits: 0 })} revenue</small></article>)}
          </div>
          <div className="table-card" style={{ marginTop: 14 }}>
            <table><thead><tr><th>Product</th><th>Category</th><th>Segment</th><th>Reason</th><th>Revenue</th><th>Units</th></tr></thead>
              <tbody>{data.products?.map((row: any) => <tr key={row.product_detail}><td><strong>{row.product_detail}</strong></td><td>{row.product_category}</td><td><span className="segment">{row.segment}</span></td><td>{row.reason}</td><td>${row.revenue.toLocaleString(undefined, { maximumFractionDigits: 2 })}</td><td>{row.quantity.toLocaleString()}</td></tr>)}</tbody>
            </table>
          </div>
        </>
      )}
      {mode === "clustering" && (
        <>
          {!data.supported ? <div className="empty-state">{data.reason}</div> : <>
            <div className="kpi-grid">
              <article className="kpi-card"><span>Cluster count</span><strong>{data.cluster_count}</strong></article>
              <article className="kpi-card"><span>Silhouette score</span><strong>{data.silhouette_score}</strong></article>
              <article className="kpi-card"><span>PCA variance</span><strong>{(data.explained_variance * 100).toFixed(1)}%</strong></article>
            </div>
            <div className="chart-grid">
              <article className="chart-card wide"><div className="card-heading"><div><span>PCA visualization</span><h2>Product Groups</h2></div></div>
                <ResponsiveContainer width="100%" height={320}><ScatterChart><CartesianGrid /><XAxis type="number" dataKey="pca_x" name="PCA 1" /><YAxis type="number" dataKey="pca_y" name="PCA 2" /><Tooltip cursor={{ strokeDasharray: "3 3" }} /><Scatter name="Products" data={data.points} fill="#6f4e37" /></ScatterChart></ResponsiveContainer>
              </article>
              <article className="chart-card"><div className="card-heading"><div><span>Elbow analysis</span><h2>Inertia by Cluster Count</h2></div></div>
                <ResponsiveContainer width="100%" height={260}><BarChart data={data.elbow}><CartesianGrid strokeDasharray="3 3" vertical={false} /><XAxis dataKey="clusters" /><YAxis /><Tooltip /><Bar dataKey="inertia" fill="#c49a55" /></BarChart></ResponsiveContainer>
              </article>
              <article className="chart-card"><div className="card-heading"><div><span>Model fit</span><h2>Silhouette Values</h2></div></div>
                <ResponsiveContainer width="100%" height={260}><BarChart data={data.silhouette_values}><CartesianGrid strokeDasharray="3 3" vertical={false} /><XAxis dataKey="clusters" /><YAxis /><Tooltip /><Bar dataKey="silhouette" fill="#241914" /></BarChart></ResponsiveContainer>
              </article>
            </div>
          </>}
        </>
      )}
      {mode === "anomalies" && (
        <>
          <article className="insights"><span className="eyebrow">METHOD NOTICE</span><p>{data.warning}</p></article>
          {!data.anomalies?.length ? <div className="empty-state">No statistical anomalies were identified.</div> :
            <div className="table-card" style={{ marginTop: 14 }}><table><thead><tr><th>Entity</th><th>Scope</th><th>Field</th><th>Value</th><th>Method</th><th>Severity</th></tr></thead>
              <tbody>{data.anomalies.map((row: any, index: number) => <tr key={`${row.product_detail}-${row.field}-${index}`}><td><strong>{row.product_detail}</strong></td><td>{row.category}</td><td>{row.field}</td><td>{row.value.toLocaleString()}</td><td>{row.method}</td><td><span className="segment">{row.severity}</span></td></tr>)}</tbody>
            </table></div>}
        </>
      )}
      {mode === "statistics" && (
        <>
          <div className="chart-grid">
            <article className="chart-card wide"><div className="card-heading"><div><span>Product aggregates</span><h2>Descriptive Statistics</h2></div></div>
              <div className="table-card"><table><thead><tr><th>Metric</th><th>Count</th><th>Mean</th><th>Std Dev</th><th>Minimum</th><th>Maximum</th></tr></thead>
                <tbody>{data.descriptive_statistics?.map((row: any) => <tr key={row.metric}><td><strong>{row.metric}</strong></td><td>{row.count}</td><td>{Number(row.mean).toFixed(2)}</td><td>{Number(row.std).toFixed(2)}</td><td>{Number(row.min).toFixed(2)}</td><td>{Number(row.max).toFixed(2)}</td></tr>)}</tbody>
              </table></div>
            </article>
            <article className="chart-card"><div className="card-heading"><div><span>Correlation matrix</span><h2>Relationships</h2></div></div>
              <div className="table-card"><table><thead><tr><th>Metric</th>{Object.keys(data.correlation_matrix?.[0] ?? {}).filter((key) => key !== "metric").map((key) => <th key={key}>{key}</th>)}</tr></thead>
                <tbody>{data.correlation_matrix?.map((row: any) => <tr key={row.metric}><td><strong>{row.metric}</strong></td>{Object.keys(row).filter((key) => key !== "metric").map((key) => <td key={key}>{row[key]}</td>)}</tr>)}</tbody>
              </table></div>
            </article>
          </div>
          <article className="insights"><span className="eyebrow">LIMITATIONS</span>{data.limitations?.map((item: string) => <p key={item}>{item}</p>)}</article>
        </>
      )}
    </div>
  );
}
