---
name: "Time Series Trends and Forecasting Workflow"
slug: "time-series-trends-and-forecasting"
version: "1.0.0"
branch: "planning"
role: "bi_analyst"
tools_required:
  - "run_trend_analysis"
  - "forecast_business_metric"
  - "compare_actual_vs_budget"
triggers:
  - "analisis tren deret waktu moving average"
  - "proyeksi perkiraan penjualan masa depan forecast"
  - "evaluasi tren pertumbuhan bisnis"
  - "forecasting metrik bisnis"
  - "time series forecast"
priority: "high"
---

# 1. Peran & Tujuan Bisnis (Role Context & Objective)
Sebagai BI Analyst, skill ini mengatur evaluasi pola pertumbuhan deret waktu (*Time-Series Trend Analysis & Moving Average*), penghitungan proyeksi kuantitatif masa depan (*Quantitative Forecasting*), serta evaluasi komparasi realisasi aktual terhadap target anggaran (*Budget vs Actual Variance*).

# 2. Alur Kerja Eksekusi (Step-by-Step Decision Tree)
1. **Analisis Tren Deret Waktu Histori (`run_trend_analysis`)**:
   * Panggil `run_trend_analysis(metric_name, historical_values, window_size)`.
   * Evaluasi arah tren: UPWARD, DOWNWARD, atau STABLE.
2. **Kalkulasi Proyeksi Masa Depan (`forecast_business_metric`)**:
   * Panggil `forecast_business_metric(metric_name, historical_series, horizon_steps)`.
3. **Komparasi Realisasi terhadap Target Anggaran (`compare_actual_vs_budget`)**:
   * Panggil `compare_actual_vs_budget(category, actual_amount, budget_amount)`.

# 3. Pra-kondisi & Validasi (Pre-conditions)
* Deret data histori harus berisi minimal 2 data poin numerik.

# 4. Batasan Kepatuhan & Guardrails (Compliance & Safety)
* Proyeksi linier bersifat estimasi statistik dan wajib dikalibrasi dengan dinamika pasar aktual.

# 5. Contoh Interaksi (Few-Shot Examples)
**User:** "Analisis tren penjualan 5 bulan terakhir [500, 520, 560, 590, 640] juta dan buatkan proyeksi 3 bulan ke depan."
**Tool Call:** `run_trend_analysis(metric_name="Monthly Revenue (Juta)", historical_values=[500, 520, 560, 590, 640], window_size=3)`
**Tool Call:** `forecast_business_metric(metric_name="Monthly Revenue (Juta)", historical_series=[500, 520, 560, 590, 640], horizon_steps=3)`
**Respon AI:** "Tren Penjualan: UPWARD (+28.0%). Proyeksi 3 bulan ke depan: Bulan 1 (Rp 675M), Bulan 2 (Rp 710M), Bulan 3 (Rp 745M)."
