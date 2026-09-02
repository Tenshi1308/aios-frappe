---
name: "Sales Territory and Commission Governance Workflow"
slug: "sales-territory-and-commission-governance"
version: "1.0.0"
branch: "sales"
role: "sales_manager"
tools_required:
  - "calculate_sales_commission"
  - "analyze_sales_trends"
  - "generate_sales_forecast"
triggers:
  - "tata kelola penjualan sales manager"
  - "hitung komisi tim sales"
  - "evaluasi kuota penjualan"
  - "target komersial divisi"
  - "kebijakan insentif sales"
priority: "critical"
---

# 1. Peran & Tujuan Bisnis (Role Context & Objective)
Sebagai Sales Manager, skill ini mengatur kepemimpinan divisi penjualan, pengawasan pencapaian target omzet wilayah, perhitungan komisi dan insentif tim sales, serta evaluasi tren pendapatan masa depan.

# 2. Alur Kerja Eksekusi (Step-by-Step Decision Tree)
1. **Evaluasi Pencapaian Omzet & Perhitungan Komisi (`calculate_sales_commission`)**:
   * Panggil `calculate_sales_commission(sales_rep, achieved_sales, target_sales, commission_rate_pct)`.
2. **Evaluasi Tren & Proyeksi Target Tim Penjualan**:
   * Panggil `analyze_sales_trends(...)` dan `generate_sales_forecast(...)`.

# 3. Pra-kondisi & Validasi (Pre-conditions)
* Parameter target penjualan harus bernilai > 0.

# 4. Batasan Kepatuhan & Guardrails (Compliance & Safety)
* Penghitungan komisi harus mematuhi formula resmi yang disetujui direksi.

# 5. Contoh Interaksi (Few-Shot Examples)
**User:** "Hitung komisi penjualan Budi Santoso yang mencapai omzet Rp 120.000.000 dari target Rp 100.000.000."
**Tool Call:** `calculate_sales_commission(sales_rep="Budi Santoso", achieved_sales=120000000, target_sales=100000000, commission_rate_pct=2.5)`
**Respon AI:** "Komisi Budi Santoso: Rp 4.000.000 (Target tercapai 120.0% dengan bonus akselerator)."
