import { BarChart3, BrainCircuit, ShieldCheck } from "lucide-react";
import { Link } from "react-router-dom";

export default function LandingPage() {
  return (
    <main className="landing">
      <nav className="landing-nav">
        <div className="landing-brand"><div className="brand-mark"><BarChart3 size={22} /></div><strong>Afficionado Intelligence</strong></div>
        <Link to="/executive">Open analytics</Link>
      </nav>
      <section className="landing-hero">
        <div>
          <span className="eyebrow">AI-POWERED PRODUCT INTELLIGENCE</span>
          <h1>Transform retail data into explainable business decisions.</h1>
          <p>A real-data analytics workspace for product performance, revenue contribution, segmentation, anomaly review, and grounded decision support.</p>
          <Link className="landing-cta" to="/executive">Explore the dashboard</Link>
        </div>
        <div className="landing-preview">
          <div className="preview-kpis"><span /><span /><span /></div>
          <div className="preview-chart"><div /><div /><div /><div /><div /></div>
        </div>
      </section>
      <section className="landing-features">
        <article><BarChart3 /><h2>Business intelligence</h2><p>Executive, product, category, store, revenue, Pareto, and ABC views.</p></article>
        <article><BrainCircuit /><h2>Advanced analytics</h2><p>Segmentation, clustering, anomaly detection, and statistical intelligence.</p></article>
        <article><ShieldCheck /><h2>Explainable limits</h2><p>No invented dates, profit claims, basket relationships, or causal pricing effects.</p></article>
      </section>
    </main>
  );
}
