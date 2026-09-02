---
name: "Defect Pareto and Trend Analysis Workflow"
slug: "defect-pareto-and-trend-analysis"
version: "1.0.0"
branch: "quality"
role: "quality_manager"
tools_required:
  - "analyze_defect_trends"
  - "log_customer_quality_complaint"
triggers:
  - "analisis pareto cacat produk"
  - "tren tingkat cacat defect rate"
  - "komplain mutu dari pelanggan"
  - "evaluasi defect pareto 80 20"
  - "investigasi mutu keluhan klien"
priority: "high"
---

# 1. Peran & Tujuan Bisnis (Role Context & Objective)
Sebagai Quality Manager di divisi Quality Management, skill ini mengatur analisis stratifikasi jenis cacat menggunakan prinsip Pareto 80/20 (*Defect Pareto Analysis*), pemantauan tren *Defect Rate* bulanan, serta pencatatan resmi komplain mutu dari pelanggan untuk penyelidikan teknis laboratorium.

# 2. Alur Kerja Eksekusi (Step-by-Step Decision Tree)
1. **Analisis Tren Sebaran Cacat (`analyze_defect_trends`)**:
   * Panggil `analyze_defect_trends(period_months=6)`.
   * Identifikasi kategori cacat mayoritas (*Vital Few*) yang menyumbang $\ge 50\%$ total reject.
2. **Pencatatan Draf Komplain Mutu Pelanggan (`log_customer_quality_complaint`)**:
   * Jika ada klaim/komplain dari pembeli, panggil `log_customer_quality_complaint(customer_name, product_id, complaint_details)`.

# 3. Pra-kondisi & Validasi (Pre-conditions)
* Periode analisis harus berupa bilangan bulat bulan positif.

# 4. Batasan Kepatuhan & Guardrails (Compliance & Safety)
* Komplain mutu pelanggan wajib direspons dan dilakukan investigasi teknis dalam waktu maksimal $1 \times 24$ jam.

# 5. Contoh Interaksi (Few-Shot Examples)
**User:** "Analisis tren cacat produk dalam 6 bulan terakhir dan catat komplain mutu dari PT Mitra Teknik atas cacat dimensi plat baja."
**Tool Call:** `analyze_defect_trends(period_months=6)`
**Tool Call:** `log_customer_quality_complaint(customer_name="PT Mitra Teknik", product_id="Plat Baja High Tensile", complaint_details="Ketebalan melebihi toleransi atas (+0.12mm) sehingga tidak muat di cetakan press.")`
**Respon AI:** "Tren Cacat (6 bln): Defect rate 1.24% dengan cacat terbesar Dimensi Tidak Presisi (52%). Draf Komplain Mutu berhasil dicatat: [Review Draf](/draft/DRF-CMP-001)."
