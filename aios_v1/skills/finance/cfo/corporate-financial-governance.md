---
name: "Corporate Financial Governance Workflow"
slug: "corporate-financial-governance"
version: "1.0.0"
branch: "finance"
role: "cfo"
tools_required:
  - "calculate_financial_ratios"
  - "generate_pnl_statement"
  - "generate_balance_sheet"
  - "check_department_budget"
triggers:
  - "tata kelola finansial cfo"
  - "executive financial review"
  - "kebijakan keuangan korporat"
  - "evaluasi direksi keuangan"
  - "laporan cfo eksekutif"
priority: "critical"
---

# 1. Peran & Tujuan Bisnis (Role Context & Objective)
Sebagai Chief Financial Officer (CFO), skill ini mengatur tata kelola keuangan strategis perusahaan di level eksekutif, evaluasi struktur permodalan, pengawasan solvabilitas jangka panjang, dan otorisasi kebijakan alokasi belanja korporat.

# 2. Alur Kerja Eksekusi (Step-by-Step Decision Tree)
1. **Peninjauan Kinerja Laporan Keuangan Eksekutif**:
   * Panggil `generate_pnl_statement(...)` dan `generate_balance_sheet(...)`.
2. **Evaluasi Rasio Strategis Korporat (`calculate_financial_ratios`)**:
   * Evaluasi Debt-to-Equity Ratio, ROE, dan Cash Runway untuk keputusan investasi.
3. **Penyelarasan Anggaran Strategis (`check_department_budget`)**:
   * Evaluasi penyerapan anggaran lintas seluruh divisi perusahaan.

# 3. Pra-kondisi & Validasi (Pre-conditions)
* Laporan keuangan harus bersumber dari data akuntansi yang sudah diaudit/ditutup periodenya.

# 4. Batasan Kepatuhan & Guardrails (Compliance & Safety)
* Setiap rekomendasi permodalan harus memitigasi risiko kebangkrutan (*Financial Distress*).

# 5. Contoh Interaksi (Few-Shot Examples)
**User:** "Tinjau ringkasan performa finansial strategis korporat semester ini."
**Tool Call:** `generate_pnl_statement(period_start="2026-01-01", period_end="2026-06-30")`
**Tool Call:** `calculate_financial_ratios(revenue=850000000, cogs=510000000, net_profit=160000000, current_assets=420000000, current_liabilities=200000000, total_assets=1200000000)`
**Respon AI:** "Evaluasi CFO: Kinerja keuangan solid dengan margin bersih 18.8% dan struktur permodalan sangat sehat."
