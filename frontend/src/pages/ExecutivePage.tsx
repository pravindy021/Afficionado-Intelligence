import { useQuery } from "@tanstack/react-query";
import { BarChart, Bar, CartesianGrid, Line, LineChart, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts";
import { ArrowUpRight, Boxes, ReceiptText, TrendingUp } from "lucide-react";
import { getJson } from "../lib/api";

type Executive = {
  kpis: Record<string, number | string>;
  revenue_trend: Array<{ hour: number; revenue: number }>;
  category_contribution: Array<{ product_category: string; revenue: number; share: number }>;
  top_products: Array<{ product_detail: string; revenue: number }>;
  store_comparison: Array<{ store_location: string; revenue: number }>;
  insights: string[];
};

const money = (value: number) => `$${value.toLocaleString(undefined, { maximumFractionDigits: 0 })}`;

export default function ExecutivePage() {
  const { data, isLoading, error } = useQuery({ queryKey: ["executive"], queryFn: () => getJson<Executive>("/analytics/executive") });
  if (isLoading) return <div className="loading">Loading analytics…</div>;
  if (error) return <div className="error-state">Unable to load analytics.</div>;
  if (!data) return null;

  const cards = [
    { label: "Total Revenue", value: money(Number(data.kpis.total_revenue)), icon: TrendingUp },
    { label: "Transactions", value: Number(data.kpis.total_transactions).toLocaleString(), icon: ReceiptText },
    { label: "Units Sold", value: Number(data.kpis.total_units).toLocaleString(), icon: Boxes },
    { label: "Active Products", value: data.kpis.active_products, icon: ArrowUpRight },
  ];

  return (
    <div className="page">
      <div className="page-heading">
        <div><span className="eyebrow">PERFORMANCE CENTER</span><h1>Executive Overview</h1></div>
        <div className="period">2025 · Source dataset</div>
      </div>
      <div className="kpi-grid">
        {cards.map(({ label, value, icon: Icon }) => (
          <article className="kpi-card" key={label}>
            <div className="kpi-icon"><Icon size={18} /></div>
            <span>{label}</span><strong>{value}</strong>
          </article>
        ))}
      </div>
      <div className="chart-grid">
        <article className="chart-card wide">
          <div className="card-heading"><div><span>Hourly revenue</span><h2>Revenue Trend</h2></div></div>
          <ResponsiveContainer width="100%" height={260}>
            <LineChart data={data.revenue_trend}>
              <CartesianGrid strokeDasharray="3 3" vertical={false} /><XAxis dataKey="hour" /><YAxis tickFormatter={(v) => `$${v / 1000}k`} /><Tooltip formatter={(v) => money(Number(v))} />
              <Line type="monotone" dataKey="revenue" stroke="#c49a55" strokeWidth={3} dot={false} />
            </LineChart>
          </ResponsiveContainer>
        </article>
        <article className="chart-card">
          <div className="card-heading"><div><span>By category</span><h2>Revenue Contribution</h2></div></div>
          <ResponsiveContainer width="100%" height={260}>
            <BarChart data={data.category_contribution} layout="vertical">
              <CartesianGrid strokeDasharray="3 3" horizontal={false} /><XAxis type="number" tickFormatter={(v) => `$${v / 1000}k`} /><YAxis type="category" dataKey="product_category" width={105} /><Tooltip formatter={(v) => money(Number(v))} />
              <Bar dataKey="revenue" fill="#6f4e37" radius={[0, 5, 5, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </article>
        <article className="chart-card">
          <div className="card-heading"><div><span>Ranked revenue</span><h2>Top Products</h2></div></div>
          <ResponsiveContainer width="100%" height={260}>
            <BarChart data={data.top_products}>
              <CartesianGrid strokeDasharray="3 3" vertical={false} /><XAxis dataKey="product_detail" hide /><YAxis tickFormatter={(v) => `$${v / 1000}k`} /><Tooltip formatter={(v) => money(Number(v))} />
              <Bar dataKey="revenue" fill="#241914" radius={[5, 5, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </article>
      </div>
      <article className="insights">
        <span className="eyebrow">EXECUTIVE INSIGHTS</span>
        {data.insights.map((insight) => <p key={insight}>{insight}</p>)}
      </article>
    </div>
  );
}
