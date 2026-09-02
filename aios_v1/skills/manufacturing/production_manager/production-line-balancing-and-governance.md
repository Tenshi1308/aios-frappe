---
name: "Production Line Balancing and Governance Workflow"
slug: "production-line-balancing-and-governance"
version: "1.0.0"
branch: "manufacturing"
role: "production_manager"
tools_required:
  - "check_work_center_capacity"
  - "generate_production_variance_report"
  - "analyze_oee_metrics"
triggers:
  - "keseimbangan lini produksi line balancing"
  - "tata kelola manufaktur pabrik"
  - "evaluasi performa lini produksi"
  - "utilisasi kapasitas pabrik menyeluruh"
  - "kebijakan operasional manufaktur"
priority: "critical"
---

# 1. Peran & Tujuan Bisnis (Role Context & Objective)
Sebagai Production Manager di divisi Manufacturing, skill ini mengatur kepemimpinan tata kelola lini produksi pabrik (*Manufacturing Governance*), penyeimbangan beban kerja antar stasiun kerja (*Line Balancing*), pengawasan efisiensi OEE pabrik, dan evaluasi pengendalian varians biaya produksi.

# 2. Alur Kerja Eksekusi (Step-by-Step Decision Tree)
1. **Evaluasi Keseimbangan Beban Lini Produksi (`check_work_center_capacity`)**:
   * Periksa beban seluruh work center untuk menghilangkan stasiun bottleneck.
2. **Evaluasi Efektivitas Mesin Menyeluruh (`analyze_oee_metrics`)**:
   * Analisis metrik OEE pabrik untuk memastikan rasio produktivitas tetap optimal.
3. **Pengendalian Varians Biaya Manufaktur (`generate_production_variance_report`)**:
   * Evaluasi selisih biaya standar dan aktual untuk menjaga margin laba operasional.

# 3. Pra-kondisi & Validasi (Pre-conditions)
* Seluruh data work center dan catatan biaya produksi harus terintegrasi.

# 4. Batasan Kepatuhan & Guardrails (Compliance & Safety)
* Peningkatan output produksi tidak boleh mengorbankan standar keselamatan kerja dan mutu produk.

# 5. Contoh Interaksi (Few-Shot Examples)
**User:** "Evaluasi efisiensi lini produksi dan varians biaya MO-005 dengan standar Rp 100.000.000 dan aktual Rp 94.000.000."
**Tool Call:** `generate_production_variance_report(production_order_id="MO-005", standard_cost=100000000, actual_cost=94000000)`
**Respon AI:** "Varians Biaya MO #MO-005 berstatus FAVORABLE (Hemat Rp 6.000.000 / 6.0% di bawah anggaran rencana)."
