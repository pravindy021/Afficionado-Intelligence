import { BarChart3, Database, LayoutDashboard, Moon, PackageSearch, CircleDollarSign, Shapes, ScanSearch, Activity, Sigma, LineChart, SlidersHorizontal, Sparkles } from "lucide-react";
import { NavLink, Outlet } from "react-router-dom";

const nav = [
  { to: "/executive", label: "Executive", icon: LayoutDashboard },
  { to: "/products", label: "Products", icon: PackageSearch },
  { to: "/revenue", label: "Revenue", icon: CircleDollarSign },
  { to: "/segmentation", label: "Segments", icon: Shapes },
  { to: "/clustering", label: "Clusters", icon: ScanSearch },
  { to: "/anomalies", label: "Anomalies", icon: Activity },
  { to: "/statistics", label: "Statistics", icon: Sigma },
  { to: "/forecast", label: "Forecasting", icon: LineChart },
  { to: "/optimization", label: "Optimization", icon: SlidersHorizontal },
  { to: "/copilot", label: "AI Copilot", icon: Sparkles },
  { to: "/data", label: "Data Center", icon: Database },
];

export default function Shell() {
  return (
    <div className="app-shell">
      <aside className="sidebar">
        <div className="brand-mark"><BarChart3 size={22} /></div>
        <div className="brand-copy">
          <strong>Afficionado</strong>
          <span>INTELLIGENCE</span>
        </div>
      </aside>
      <main className="workspace">
        <header className="topbar">
          <nav>
            {nav.map(({ to, label, icon: Icon }) => (
              <NavLink key={to} to={to} className={({ isActive }) => isActive ? "nav-link active" : "nav-link"}>
                <Icon size={17} />
                {label}
              </NavLink>
            ))}
          </nav>
          <button className="icon-button" aria-label="Theme" onClick={() => document.documentElement.classList.toggle("dark")}><Moon size={18} /></button>
        </header>
        <section className="content"><Outlet /></section>
      </main>
    </div>
  );
}
