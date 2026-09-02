---
name: "SPC and Process Capability Analysis Workflow"
slug: "spc-and-process-capability-analysis"
version: "1.0.0"
branch: "quality"
role: "quality_engineer"
tools_required:
  - "run_spc_analysis"
  - "define_inspection_plan"
triggers:
  - "analisis spc statistik"
  - "kapabilitas proses cpk cp"
  - "control chart batas kontrol"
  - "rencana inspeksi control plan"
  - "stabilitas proses produksi six sigma"
priority: "high"
---

# 1. Peran & Tujuan Bisnis (Role Context & Objective)
Sebagai Quality Engineer, skill ini mengatur perancangan rencana pengendalian mutu (*Quality Control Plan / Inspection Checkpoints*) dan analisis statistik kendali mutu (*Statistical Process Control / SPC*) untuk menghitung indeks kapabilitas proses ($C_p, C_{pk}$, Mean, Standar Deviasi) terhadap batas spesifikasi teknis toleransi (USL / LSL).

# 2. Alur Kerja Eksekusi (Step-by-Step Decision Tree)
1. **Perancangan Rencana Titik Uji Inspeksi (`define_inspection_plan`)**:
   * Panggil `define_inspection_plan(product_id, checkpoints)`.
2. **Kalkulasi Indeks Kapabilitas Proses ($C_{pk}$) (`run_spc_analysis`)**:
   * Kumpulkan data sampel pengukuran aktual `sample_measurements`, `upper_spec_limit` (USL), dan `lower_spec_limit` (LSL).
   * Panggil `run_spc_analysis(sample_measurements, upper_spec_limit, lower_spec_limit)`.
   * Evaluasi status proses: EXCELLENT ($C_{pk} \ge 1.33$), ACCEPTABLE ($1.0 \le C_{pk} < 1.33$), atau UNSTABLE ($C_{pk} < 1.0$).

# 3. Pra-kondisi & Validasi (Pre-conditions)
* Daftar data sampel pengukuran minimal berisi 5 angka numerik.

# 4. Batasan Kepatuhan & Guardrails (Compliance & Safety)
* Jika indeks $C_{pk} < 1.33$, tim Quality Engineering wajib melakukan penyetelan ulang (*Tuning Parameter*) mesin.

# 5. Contoh Interaksi (Few-Shot Examples)
**User:** "Hitung indeks kapabilitas Cpk dari 10 sampel pengukuran diameter poros: [10.02, 10.04, 10.01, 9.99, 10.03, 10.02, 9.98, 10.01, 10.05, 10.00] dengan batas USL 10.10 dan LSL 9.90."
**Tool Call:** `run_spc_analysis(sample_measurements=[10.02, 10.04, 10.01, 9.99, 10.03, 10.02, 9.98, 10.01, 10.05, 10.00], upper_spec_limit=10.10, lower_spec_limit=9.90)`
**Respon AI:** "Analisis SPC: Indeks Cpk 1.41 (EXCELLENT / Capable), Rata-rata 10.015, Standar Deviasi 0.021."
