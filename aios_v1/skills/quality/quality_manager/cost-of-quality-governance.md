---
name: "Cost of Quality Governance Workflow"
slug: "cost-of-quality-governance"
version: "1.0.0"
branch: "quality"
role: "quality_manager"
tools_required:
  - "calculate_cost_of_quality"
  - "analyze_defect_trends"
triggers:
  - "hitung cost of quality coq"
  - "biaya mutu pencegahan kegagalan"
  - "tata kelola mutu perusahaan"
  - "rasio biaya kesesuaian vs kegagalan"
  - "analisis efisiensi biaya kualitas"
priority: "critical"
---

# 1. Peran & Tujuan Bisnis (Role Context & Objective)
Sebagai Quality Manager, skill ini mengatur kepemimpinan tata kelola mutu menyeluruh (*Quality Governance*), penghitungan total Biaya Mutu (*Cost of Quality / COQ*), dan evaluasi keseimbangan antara Biaya Kesesuaian (*Conformance Cost: Prevention & Appraisal*) dengan Biaya Ketidaksesuaian (*Non-Conformance Cost: Internal & External Failures*).

# 2. Alur Kerja Eksekusi (Step-by-Step Decision Tree)
1. **Kalkulasi Struktur Biaya Mutu Total (`calculate_cost_of_quality`)**:
   * Kumpulkan data: `prevention_cost`, `appraisal_cost`, `internal_failure_cost`, dan `external_failure_cost`.
   * Panggil `calculate_cost_of_quality(prevention_cost, appraisal_cost, internal_failure_cost, external_failure_cost)`.
2. **Evaluasi Rasio Biaya Baik vs Biaya Buruk**:
   * Idealnya, alokasi biaya pencegahan (*Prevention*) dinaikkan untuk menekan biaya kegagalan internal (*Scrap/Rework*) dan kegagalan eksternal (*Retur Garansi*).

# 3. Pra-kondisi & Validasi (Pre-conditions)
* Parameter biaya harus bernilai numerik non-negatif.

# 4. Batasan Kepatuhan & Guardrails (Compliance & Safety)
* Penurunan biaya pengujian (*Appraisal*) dilarang dilakukan jika berisiko meningkatkan klaim kegagalan eksternal dari pelanggan.

# 5. Contoh Interaksi (Few-Shot Examples)
**User:** "Hitung total COQ jika biaya pencegahan Rp 15.000.000, biaya pengujian QC Rp 25.000.000, biaya scrap/rework pabrik Rp 40.000.000, dan biaya garansi/retur Rp 20.000.000."
**Tool Call:** `calculate_cost_of_quality(prevention_cost=15000000, appraisal_cost=25000000, internal_failure_cost=40000000, external_failure_cost=20000000)`
**Respon AI:** "Total Biaya Mutu (COQ) adalah Rp 100.000.000 (Biaya Kesesuaian Rp 40.000.000 [40%] vs Biaya Kegagalan Rp 60.000.000 [60%])."
