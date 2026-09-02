---
name: "Financial Statement Analysis Workflow"
slug: "financial-statement-analysis"
version: "1.0.0"
branch: "finance"
role: "financial_analyst"
tools_required:
  - "generate_pnl_statement"
  - "generate_balance_sheet"
  - "calculate_financial_ratios"
triggers:
  - "analisis laporan keuangan"
  - "pnl statement"
  - "neraca saldo"
  - "rasio keuangan"
  - "evaluasi kinerja finansial"
priority: "high"
---

# 1. Peran & Tujuan Bisnis (Role Context & Objective)
Sebagai Financial Analyst, skill ini mengatur alur evaluasi komprehensif atas laporan keuangan perusahaan. Peran ini bertugas menganalisis laporan Laba/Rugi (P&L) dan Neraca Saldo (*Balance Sheet*), serta mengkalkulasi rasio-rasio kunci (Current Ratio, Net Profit Margin, ROA, DER) guna memberikan gambaran kesehatan finansial kepada manajemen.

# 2. Alur Kerja Eksekusi (Step-by-Step Decision Tree)
1. **Penyusunan Laporan P&L & Neraca**:
   * Panggil `generate_pnl_statement(period_start, period_end)` untuk melihat pendapatan, beban, dan profitabilitas.
   * Panggil `generate_balance_sheet(as_of_date)` untuk melihat posisi aset, liabilitas, dan ekuitas.
2. **Kalkulasi Rasio Keuangan (`calculate_financial_ratios`)**:
   * Panggil `calculate_financial_ratios(revenue, cogs, net_profit, current_assets, current_liabilities, total_assets)`.
   * Bandingkan hasil likuiditas dan solvabilitas dengan standar industri.

# 3. Pra-kondisi & Validasi (Pre-conditions)
* Parameter rentang tanggal harus valid.
* Seluruh transaksi nominal dan riil telah selesai diposting.

# 4. Batasan Kepatuhan & Guardrails (Compliance & Safety)
* **DILARANG** menyajikan interpretasi tanpa membandingkan data historis yang relevan.

# 5. Contoh Interaksi (Few-Shot Examples)
**User:** "Tolong buatkan analisis laporan keuangan dan rasio untuk semester ini."
**Tool Call:** `generate_pnl_statement(period_start="2026-01-01", period_end="2026-06-30")`
**Tool Call:** `calculate_financial_ratios(revenue=850000000, cogs=510000000, net_profit=160000000, current_assets=420000000, current_liabilities=200000000, total_assets=1200000000)`
**Respon AI:** "Laporan Keuangan Semester 1 2026 menunjukkan kondisi sehat dengan Net Profit Margin 18.8% dan Current Ratio 2.1x."
