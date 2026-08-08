"use client";
import { useEffect, useState } from "react";
import dynamic from "next/dynamic";

const Plot = dynamic(() => import("react-plotly.js"), { ssr: false });
const API_BASE = "http://127.0.0.1:8000/api";

export default function HomePage() {
  const [topProducts, setTopProducts] = useState({ labels: [], values: [] });
  const [cashFlow, setCashFlow] = useState({ labels: [], cash_in: [], cash_out: [] });

  useEffect(() => {
    async function loadData() {
      const [topRes, cashRes] = await Promise.all([
        fetch(`${API_BASE}/bi/top-products/?period=month`, { credentials: "include" }),
        fetch(`${API_BASE}/bi/cash-flow/?period=month`, { credentials: "include" }),
      ]);
      if (!topRes.ok) {
        throw new Error(`Falha ao carregar top-products: HTTP ${topRes.status}`);
      }
      if (!cashRes.ok) {
        throw new Error(`Falha ao carregar cash-flow: HTTP ${cashRes.status}`);
      }
      setTopProducts(await topRes.json());
      setCashFlow(await cashRes.json());
    }
    loadData().catch(console.error);
  }, []);

  return (
    <main>
      <h1>Painel BI - Estoque da Igreja</h1>
      <p>Esqueleto inicial com dados vindos da API Django.</p>
      <h2>Produtos mais vendidos (mes)</h2>
      <Plot
        data={[{ x: topProducts.labels, y: topProducts.values, type: "bar" }]}
        layout={{ width: 850, height: 400, title: "Top 10 produtos" }}
      />
      <h2>Fluxo de caixa (entrou x saiu)</h2>
      <Plot
        data={[
          { x: cashFlow.labels, y: cashFlow.cash_in, type: "scatter", mode: "lines+markers", name: "Entradas" },
          { x: cashFlow.labels, y: cashFlow.cash_out, type: "scatter", mode: "lines+markers", name: "Saidas" },
        ]}
        layout={{ width: 850, height: 400, title: "Fluxo de caixa" }}
      />
    </main>
  );
}
