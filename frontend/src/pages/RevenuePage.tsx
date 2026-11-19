import { useQuery } from "@tanstack/react-query";
import { Bar, BarChart, CartesianGrid, Line, LineChart, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts";
import { getJson } from "../lib/api";

type RevenueData = {
  metrics: { total_revenue: number; total_quantity: number; transaction_count: number; average_selling_price: number };
  category_comparison: Array<{ product_category: string; revenue: number; revenue_share: number }>;
  store_comparison: Array<{ store_location: string; revenue: number; revenue_share: number }>;
  pareto: Array<{ product_detail: string; revenue: number; cumulative_revenue_share: number; abc_class: string }>;
  hourly_trend: Array<{ hour: number; revenue: number }>;
  concentration: { top_10_product_revenue_share: number; top_product_revenue: number };
  top_products: Array<{ product_detail: string; revenue: number }>;
  bottom_products: Array<{ product_detail: string; revenue: number }>;
  limitations: { date_trend_supported: boolean; hourly_trend_supported: boolean; reason: string };
};

const money = (value: number) => `$${value.toLocaleString(undefined, { maximumFractionDigits: 0 })}`;

export default function RevenuePage() {
  const { data, isLoading, error } = useQuery({ queryKey: ["revenue"], queryFn: () => getJson<RevenueData>("/analytics/revenue") });
  if (isLoading) return <div className="loading">Loading revenue intelligence…</div>;
  if (error) return <div className="error-state">Unable to load revenue intelligence.</div>;
  if (!data) return null;
  return (
    <div className="page">
      <div className="page-heading"><div><span className="eyebrow">REVENUE INTELLIGENCE</span><h1>Contribution & Concentration</h1></div></div>
      <div className="kpi-grid">
        <article className="kpi-card"><span>Total revenue</span><strong>{money(data.metrics.total_revenue)}</strong></article>
        <article className="kpi-card"><span>Top 10 product share</span><strong>{(data.concentration.top_10_product_revenue_share * 100).toFixed(1)}%</strong></article>
        <article className="kpi-card"><span>Transactions</span><strong>{data.metrics.transaction_count.toLocaleString()}</strong></article>
        <article className="kpi-card"><span>Units sold</span><strong>{data.metrics.total_quantity.toLocaleString()}</strong></article>
      </div>
      <div className="chart-grid">
        <article className="chart-card wide">
          <div className="card-heading"><div><span>Source time field</span><h2>Hourly Revenue</h2></div></div>
          <ResponsiveContainer width="100%" height={260}>
            <LineChart data={data.hourly_trend}>
              <CartesianGrid strokeDasharray="3 3" vertical={false} /><XAxis dataKey="hour" /><YAxis tickFormatter={(v) => `$${v / 1000}k`} /><Tooltip formatter={(v) => money(Number(v))} />
              <Line type="monotone" dataKey="revenue" stroke="#c49a55" strokeWidth={3} dot={false} />
            </LineChart>
          </ResponsiveContainer>
        </article>
        <article className="chart-card">
          <div className="card-heading"><div><span>By category</span><h2>Category Revenue</h2></div></div>
          <ResponsiveContainer width="100%" height={260}>
            <BarChart data={data.category_comparison} layout="vertical">
              <CartesianGrid strokeDasharray="3 3" horizontal={false} /><XAxis type="number" tickFormatter={(v) => `$${v / 1000}k`} /><YAxis type="category" dataKey="product_category" width={105} /><Tooltip formatter={(v) => money(Number(v))} />
              <Bar dataKey="revenue" fill="#6f4e37" radius={[0, 5, 5, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </article>
        <article className="chart-card">
          <div className="card-heading"><div><span>Ranked products</span><h2>Pareto Revenue</h2></div></div>
          <ResponsiveContainer width="100%" height={260}>
            <BarChart data={data.pareto}>
              <CartesianGrid strokeDasharray="3 3" vertical={false} /><XAxis dataKey="product_detail" hide /><YAxis tickFormatter={(v) => `$${v / 1000}k`} /><Tooltip formatter={(v) => money(Number(v))} />
              <Bar dataKey="revenue" fill="#241914" radius={[5, 5, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </article>
      </div>
      <article className="insights">
        <span className="eyebrow">LIMITATION</span>
        <p>{data.limitations.reason}</p>
      </article>
    </div>
  );
}
