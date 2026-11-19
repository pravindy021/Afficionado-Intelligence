import { useQuery } from "@tanstack/react-query";
import { useState } from "react";
import { getJson } from "../lib/api";

type Product = { product_detail: string; product_category: string; product_type: string; units: number; revenue: number; average_price: number; revenue_share: number; quantity_share: number; segment: string };

export default function ProductsPage() {
  const [search, setSearch] = useState("");
  const [category, setCategory] = useState("");
  const { data, isLoading, error } = useQuery({
    queryKey: ["products", search, category],
    queryFn: () => getJson<{ products: Product[] }>(`/analytics/products?search=${encodeURIComponent(search)}&category=${encodeURIComponent(category)}`),
  });
  if (isLoading) return <div className="loading">Loading products…</div>;
  if (error) return <div className="error-state">Unable to load product analytics.</div>;
  const categories = [...new Set(data?.products.map((product) => product.product_category) ?? [])].sort();
  return (
    <div className="page">
      <div className="page-heading"><div><span className="eyebrow">PORTFOLIO ANALYSIS</span><h1>Product Intelligence</h1></div></div>
      <div className="filters">
        <input value={search} onChange={(event) => setSearch(event.target.value)} placeholder="Search product" aria-label="Search products" />
        <select value={category} onChange={(event) => setCategory(event.target.value)} aria-label="Filter category">
          <option value="">All categories</option>
          {categories.map((name) => <option key={name} value={name}>{name}</option>)}
        </select>
      </div>
      {!data?.products.length ? <div className="empty-state">No products match these filters.</div> : null}
      <div className="table-card">
        <table>
          <thead><tr><th>Product</th><th>Category</th><th>Type</th><th>Segment</th><th>Units</th><th>Avg. price</th><th>Revenue</th><th>Revenue share</th></tr></thead>
          <tbody>{data?.products.map((product) => (
            <tr key={product.product_detail}>
              <td><strong>{product.product_detail}</strong></td><td>{product.product_category}</td><td>{product.product_type}</td>
              <td><span className="segment">{product.segment}</span></td><td>{product.units.toLocaleString()}</td>
              <td>${product.average_price.toFixed(2)}</td><td>${product.revenue.toLocaleString(undefined, { maximumFractionDigits: 2 })}</td>
              <td>{(product.revenue_share * 100).toFixed(1)}%</td>
            </tr>
          ))}</tbody>
        </table>
      </div>
    </div>
  );
}
