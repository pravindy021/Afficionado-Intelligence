import { BrowserRouter, Route, Routes } from "react-router-dom";
import ExecutivePage from "./pages/ExecutivePage";
import ProductsPage from "./pages/ProductsPage";
import DataPage from "./pages/DataPage";
import RevenuePage from "./pages/RevenuePage";
import AdvancedPage from "./pages/AdvancedPage";
import ForecastPage from "./pages/ForecastPage";
import OptimizationPage from "./pages/OptimizationPage";
import CopilotPage from "./pages/CopilotPage";
import LandingPage from "./pages/LandingPage";
import Shell from "./components/Shell";

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<LandingPage />} />
        <Route element={<Shell />}>
          <Route path="/executive" element={<ExecutivePage />} />
          <Route path="/products" element={<ProductsPage />} />
          <Route path="/revenue" element={<RevenuePage />} />
          <Route path="/segmentation" element={<AdvancedPage mode="segmentation" />} />
          <Route path="/clustering" element={<AdvancedPage mode="clustering" />} />
          <Route path="/anomalies" element={<AdvancedPage mode="anomalies" />} />
          <Route path="/statistics" element={<AdvancedPage mode="statistics" />} />
          <Route path="/forecast" element={<ForecastPage />} />
          <Route path="/optimization" element={<OptimizationPage />} />
          <Route path="/copilot" element={<CopilotPage />} />
          <Route path="/data" element={<DataPage />} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
}
