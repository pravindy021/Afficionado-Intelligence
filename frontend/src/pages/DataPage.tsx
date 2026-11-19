import { useQuery } from "@tanstack/react-query";
import { getJson } from "../lib/api";

type Profile = { dataset_version: Record<string, unknown>; dataset: Record<string, unknown>; validation: Record<string, unknown> };

export default function DataPage() {
  const { data, isLoading, error } = useQuery({ queryKey: ["profile"], queryFn: () => getJson<Profile>("/data/profile") });
  if (isLoading) return <div className="loading">Loading data profile…</div>;
  if (error) return <div className="error-state">Unable to load dataset profile.</div>;
  return (
    <div className="page">
      <div className="page-heading"><div><span className="eyebrow">DATA MANAGEMENT</span><h1>Dataset Profile</h1></div></div>
      <div className="profile-grid">
        {Object.entries(data?.dataset_version ?? {}).map(([key, value]) => (
          <article className="profile-card" key={`version-${key}`}><span>version · {key.replaceAll("_", " ")}</span><strong>{typeof value === "object" ? JSON.stringify(value) : String(value)}</strong></article>
        ))}
        {Object.entries(data?.dataset ?? {}).map(([key, value]) => (
          <article className="profile-card" key={key}><span>{key.replaceAll("_", " ")}</span><strong>{typeof value === "object" ? JSON.stringify(value) : String(value)}</strong></article>
        ))}
      </div>
      <article className="insights"><span className="eyebrow">VALIDATION LIMITATIONS</span>
        {Object.entries(data?.validation ?? {}).map(([key, value]) => <p key={key}><b>{key.replaceAll("_", " ")}:</b> {String(value)}</p>)}
      </article>
    </div>
  );
}
