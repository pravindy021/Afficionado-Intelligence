import { useQuery } from "@tanstack/react-query";
import { getJson } from "../lib/api";

export default function ForecastPage() {
  const { data, isLoading, error } = useQuery({ queryKey: ["forecast-suitability"], queryFn: () => getJson<Record<string, any>>("/forecast/suitability") });
  if (isLoading) return <div className="loading">Assessing forecast suitability…</div>;
  if (error) return <div className="error-state">Unable to assess forecast suitability.</div>;
  if (!data) return null;
  return (
    <div className="page">
      <div className="page-heading"><div><span className="eyebrow">PREDICTIVE INTELLIGENCE</span><h1>Forecast Assessment</h1></div></div>
      <div className="kpi-grid">
        <article className="kpi-card"><span>Forecast supported</span><strong>{data.supported ? "Yes" : "No"}</strong></article>
        <article className="kpi-card"><span>Finest defensible granularity</span><strong>{data.finest_supported_granularity}</strong></article>
        <article className="kpi-card"><span>Calendar dates</span><strong>{data.available_history.calendar_dates ? "Available" : "Unavailable"}</strong></article>
        <article className="kpi-card"><span>Source years</span><strong>{data.available_history.year_values.join(", ")}</strong></article>
      </div>
      <article className="insights">
        <span className="eyebrow">SUITABILITY RESULT</span>
        <p>{data.reason}</p>
        <p><strong>Safe alternative:</strong> {data.safe_alternative}</p>
      </article>
      <div className="empty-state">No forecast values are displayed because the source does not support defensible time-series forecasting.</div>
    </div>
  );
}
