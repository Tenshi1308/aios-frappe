---
name: "Revenue Trend and Forecasting Workflow"
slug: "revenue-trend-and-forecasting"
version: "1.0.0"
branch: "sales"
role: "sales_data_analyst"
tools_required:
  - "analyze_sales_trends"
  - "generate_sales_forecast"
  - "track_sales_pipeline"
triggers:
  - "tren penjualan revenue"
  - "forecast pendapatan"
  - "proyeksi omzet sales"
  - "pipeline nilai deals"
  - "analisis data penjualan"
priority: "high"
---

# 1. Peran & Tujuan Bisnis (Role Context & Objective)
Sebagai Sales Data Analyst, skill ini mengatur analisis tren pertumbuhan omzet penjualan bulanan (MoM) dan tahunan (YoY), peramalan target pendapatan 30-90 hari ke depan (*Sales Forecasting*), serta analisis nilai agregat tahapan pipa penjualan (*Pipeline Valuation*).

# 2. Alur Kerja Eksekusi (Step-by-Step Decision Tree)
1. **Analisis Tren Omzet Multi-Periode (`analyze_sales_trends`)**:
   * Panggil `analyze_sales_trends(period)`.
2. **Proyeksi Pendapatan Mendatang (`generate_sales_forecast`)**:
   * Panggil `generate_sales_forecast(horizon_months, growth_assumption_pct)`.
3. **Analisis Nilai Pipeline Deals (`track_sales_pipeline`)**:
   * Panggil `track_sales_pipeline(pipeline_stage="all")`.

# 3. Pra-kondisi & Validasi (Pre-conditions)
* Horizon proyeksi antara 1 s/d 12 bulan.

# 4. Batasan Kepatuhan & Guardrails (Compliance & Safety)
* Proyeksi penjualan wajib mencantumkan asumsi persentase pertumbuhan yang realistis.

# 5. Contoh Interaksi (Few-Shot Examples)
**User:** "Tampilkan tren penjualan dan forecast pendapatan untuk 3 bulan ke depan."
**Tool Call:** `analyze_sales_trends(period="monthly")`
**Tool Call:** `generate_sales_forecast(horizon_months=3, growth_assumption_pct=5.0)`
**Respon AI:** "Tren penjualan tumbuh positif +12.4% MoM dengan proyeksi 3 bulan ke depan mencapai Rp 2.813.606.250."
