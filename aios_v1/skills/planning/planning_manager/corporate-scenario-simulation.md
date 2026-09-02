---
name: "Corporate Scenario Simulation Workflow"
slug: "corporate-scenario-simulation"
version: "1.0.0"
branch: "planning"
role: "planning_manager"
tools_required:
  - "run_what_if_scenario"
  - "forecast_business_metric"
  - "generate_kpi_dashboard"
triggers:
  - "simulasi skenario bisnis what if"
  - "uji sensitivitas kenaikan harga inflasi"
  - "dampak perubahan biaya terhadap laba"
  - "simulasi laba rugi strategis"
  - "corporate scenario what if"
priority: "critical"
---

# 1. Peran & Tujuan Bisnis (Role Context & Objective)
Sebagai Planning Manager, skill ini mengatur simulasi skenario bisnis strategis (*What-If Scenario Simulation & Sensitivity Analysis*) untuk mengevaluasi dampak simultan kenaikan/penurunan harga jual, inflasi biaya bahan baku, dan elastisitas volume permintaan terhadap laba bersih korporat, guna memandu keputusan ekspansi atau mitigasi risiko Direksi.

# 2. Alur Kerja Eksekusi (Step-by-Step Decision Tree)
1. **Simulasi Analisis Sensitivitas Skenario (`run_what_if_scenario`)**:
   * Panggil `run_what_if_scenario(scenario_name, base_revenue, base_cost, price_change_pct, cost_change_pct, volume_change_pct)`.
   * Evaluasi dampak terhadap laba bersih (`profit_impact_delta`) dan status rekomendasi: `GO_FORWARD` atau `HIGH_RISK`.
2. **Kompilasi Dashboard Proyeksi Terkait**:
   * Panggil `forecast_business_metric` atau `generate_kpi_dashboard` untuk visualisasi komparatif.

# 3. Pra-kondisi & Validasi (Pre-conditions)
* Parameter pendapatan dan biaya dasar harus bernilai numerik positif.

# 4. Batasan Kepatuhan & Guardrails (Compliance & Safety)
* Skenario dengan proyeksi penurunan laba drastis wajib disertai rekomendasi opsi efisiensi alternatif.

# 5. Contoh Interaksi (Few-Shot Examples)
**User:** "Simulasikan skenario 'Kenaikan Harga +10% dengan Inflasi Biaya +5% dan Penurunan Volume -2%' pada basis pendapatan Rp 10 Miliar dan biaya Rp 7 Miliar."
**Tool Call:** `run_what_if_scenario(scenario_name="Kenaikan Harga +10% Inflasi +5% Volume -2%", base_revenue=10000000000, base_cost=7000000000, price_change_pct=10.0, cost_change_pct=5.0, volume_change_pct=-2.0)`
**Respon AI:** "Simulasi Skenario: Proyeksi Pendapatan Rp 10.78M, Proyeksi Biaya Rp 7.20M, Proyeksi Laba Rp 3.58M. Dampak Laba Bersih: +Rp 581.000.000 (Rekomendasi: GO_FORWARD)."
