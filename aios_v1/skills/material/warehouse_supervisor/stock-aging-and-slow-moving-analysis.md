---
name: "Stock Aging and Slow-Moving Analysis Workflow"
slug: "stock-aging-and-slow-moving-analysis"
version: "1.0.0"
branch: "material"
role: "warehouse_supervisor"
tools_required:
  - "generate_stock_aging_report"
  - "generate_abc_analysis"
triggers:
  - "analisis umur stok"
  - "barang slow moving"
  - "dead stock gudang"
  - "analisis persediaan abc"
  - "modal kerja tertahan stok"
priority: "high"
---

# 1. Peran & Tujuan Bisnis (Role Context & Objective)
Sebagai Warehouse Supervisor, skill ini mengatur identifikasi barang persediaan yang lambat bergerak (*Slow-Moving*) atau tidak bergerak (*Dead Stock*), klasifikasi persediaan ABC, serta kalkulasi nilai modal kerja yang tertahan di gudang.

# 2. Alur Kerja Eksekusi (Step-by-Step Decision Tree)
1. **Analisis Klasifikasi Persediaan ABC (`generate_abc_analysis`)**:
   * Panggil `generate_abc_analysis()`.
2. **Penyusunan Laporan Umur Persediaan (`generate_stock_aging_report`)**:
   * Panggil `generate_stock_aging_report(days_threshold=90)`.
   * Rekomendasikan program cuci gudang (*clearance*) atau pengembalian ke vendor untuk barang mati.

# 3. Pra-kondisi & Validasi (Pre-conditions)
* Ambang batas hari inaktif (`days_threshold`) default 90 hari.

# 4. Batasan Kepatuhan & Guardrails (Compliance & Safety)
* Seluruh item *Dead Stock* wajib dilaporkan berkala ke Finance Manager untuk pencadangan penurunan nilai persediaan.

# 5. Contoh Interaksi (Few-Shot Examples)
**User:** "Tampilkan daftar item barang slow-moving yang tidak bergerak lebih dari 90 hari."
**Tool Call:** `generate_stock_aging_report(days_threshold=90)`
**Respon AI:** "Ditemukan 1 SKU slow-moving (Plat Besi 3mm Lembaran) dengan nilai modal tertahan Rp 24.000.000 (Dormant 120 hari)."
