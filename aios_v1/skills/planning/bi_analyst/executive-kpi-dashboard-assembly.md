---
name: "Executive KPI Dashboard Assembly Workflow"
slug: "executive-kpi-dashboard-assembly"
version: "1.0.0"
branch: "planning"
role: "bi_analyst"
tools_required:
  - "generate_kpi_dashboard"
  - "run_cross_department_report"
triggers:
  - "dashboard kpi eksekutif bisnis"
  - "laporan analitik lintas departemen"
  - "korelasi penjualan dan inventori"
  - "ringkasan kinerja perusahaan"
  - "executive bi dashboard"
priority: "high"
---

# 1. Peran & Tujuan Bisnis (Role Context & Objective)
Sebagai Business Intelligence (BI) Analyst di divisi Strategic & Operational Planning, skill ini mengatur kompilasi metrik kinerja utama lintas fungsi bisnis (*Executive KPI Dashboard: Financial, Operations, OTIF, OEE, Human Capital*), serta analisis agregasi korelasi lintas departemen (*Cross-Department Correlation Analytics*).

# 2. Alur Kerja Eksekusi (Step-by-Step Decision Tree)
1. **Kompilasi Metrik Dashboard KPI Eksekutif (`generate_kpi_dashboard`)**:
   * Panggil `generate_kpi_dashboard()`.
   * Ekstrak metrik Finansial (Revenue YTD, Gross Margin, Net Profit), Operasional (OTIF, FPY, OEE), dan SDM (Headcount, Turnover).
2. **Analisis Korelasi Lintas Fungsi (`run_cross_department_report`)**:
   * Panggil `run_cross_department_report(primary_domain, correlated_domain, aggregation_period)`.

# 3. Pra-kondisi & Validasi (Pre-conditions)
* Data transaksi dari Data Access Agent harus berstatus aktif.

# 4. Batasan Kepatuhan & Guardrails (Compliance & Safety)
* Informasi kinerja finansial bersifat rahasia dan hanya disajikan untuk pihak berwenang.

# 5. Contoh Interaksi (Few-Shot Examples)
**User:** "Tampilkan ringkasan KPI Dashboard Eksekutif dan analisis korelasi antara Sales dan Inventory per kuartal."
**Tool Call:** `generate_kpi_dashboard()`
**Tool Call:** `run_cross_department_report(primary_domain="Sales", correlated_domain="Inventory", aggregation_period="quarterly")`
**Respon AI:** "Dashboard Eksekutif: Revenue Rp 8.5M (Gross Margin 38.5%, OTIF 94.7%, OEE 83.3%). Korelasi Sales vs Inventory kuat positif ($r = 0.88$)."
