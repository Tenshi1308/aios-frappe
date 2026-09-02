---
name: "Vendor SLA and ABC Classification Workflow"
slug: "vendor-sla-and-abc-classification"
version: "1.0.0"
branch: "material"
role: "sourcing_specialist"
tools_required:
  - "evaluate_vendor_performance"
  - "generate_abc_analysis"
  - "calculate_safety_stock"
triggers:
  - "evaluasi kinerja vendor"
  - "skor kepatuhan supplier"
  - "klasifikasi abc material"
  - "vendor scorecard"
  - "safety stock supplier"
priority: "high"
---

# 1. Peran & Tujuan Bisnis (Role Context & Objective)
Sebagai Sourcing Specialist, skill ini mengatur penilaian berkala performa pemasok (*Vendor Performance Evaluation*), analisis klasifikasi material ABC, serta penentuan cadangan stok pengaman berdasarkan tingkat keandalan pengiriman masing-masing vendor.

# 2. Alur Kerja Eksekusi (Step-by-Step Decision Tree)
1. **Penilaian Skor Kinerja Vendor (`evaluate_vendor_performance`)**:
   * Panggil `evaluate_vendor_performance(vendor_name, on_time_delivery_pct, quality_defect_rate_pct, price_competitiveness_score)`.
   * Tetapkan kategori *Vendor Grade* (Grade A Preferred / Grade B Qualified / Grade C Under Review).
2. **Penyelarasan Klasifikasi Material & Safety Stock**:
   * Panggil `generate_abc_analysis()` dan `calculate_safety_stock(...)`.

# 3. Pra-kondisi & Validasi (Pre-conditions)
* Parameter penilaian performa berupa angka persentase valid (0 - 100).

# 4. Batasan Kepatuhan & Guardrails (Compliance & Safety)
* Vendor dengan Grade C (*Under Review*) wajib mendapatkan peringatan perbaikan mutu atau dihentikan alokasi PO barunya.

# 5. Contoh Interaksi (Few-Shot Examples)
**User:** "Evaluasi kinerja PT Sumber Makmur dengan ketepatan waktu 95%, tingkat reject 1.2%, dan skor harga 88."
**Tool Call:** `evaluate_vendor_performance(vendor_name="PT Sumber Makmur", on_time_delivery_pct=95.0, quality_defect_rate_pct=1.2, price_competitiveness_score=88.0)`
**Respon AI:** "Evaluasi Vendor 'PT Sumber Makmur': Skor 90.8/100 (Grade: A Preferred)."
