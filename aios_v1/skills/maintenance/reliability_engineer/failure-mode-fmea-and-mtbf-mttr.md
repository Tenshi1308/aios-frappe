---
name: "Failure Mode FMEA and MTBF MTTR Workflow"
slug: "failure-mode-fmea-and-mtbf-mttr"
version: "1.0.0"
branch: "maintenance"
role: "reliability_engineer"
tools_required:
  - "analyze_equipment_failure"
  - "calculate_mtbf_mttr"
triggers:
  - "hitung mtbf dan mttr keandalan mesin"
  - "analisis fmea pola kerusakan mesin"
  - "inherent availability keandalan"
  - "evaluasi akar masalah breakdown"
  - "reliability metrics fmea"
priority: "high"
---

# 1. Peran & Tujuan Bisnis (Role Context & Objective)
Sebagai Reliability Engineer di divisi Pemeliharaan Mesin, skill ini mengatur analisis akar penyebab pola kerusakan berulang menggunakan metodologi *Failure Mode and Effects Analysis* (FMEA / Root Cause Analysis), serta penghitungan metrik kuantitatif keandalan mesin: *Mean Time Between Failures* (MTBF), *Mean Time To Repair* (MTTR), dan *Inherent Availability*.

# 2. Alur Kerja Eksekusi (Step-by-Step Decision Tree)
1. **Analisis Riwayat Kegagalan FMEA (`analyze_equipment_failure`)**:
   * Panggil `analyze_equipment_failure(equipment_id, period_months)`.
   * Evaluasi skor Risk Priority Number (RPN) dan tindakan mitigasi.
2. **Kalkulasi Metrik Reliabilitas MTBF & MTTR (`calculate_mtbf_mttr`)**:
   * Panggil `calculate_mtbf_mttr(total_operating_hours, number_of_breakdowns, total_repair_downtime_hours)`.
   * Evaluasi rating keandalan: `WORLD_CLASS` ($\text{MTBF} \ge 500\text{ jam}, \text{MTTR} \le 2\text{ jam}$) atau `ACCEPTABLE`.

# 3. Pra-kondisi & Validasi (Pre-conditions)
* Jumlah jam operasi dan jumlah insiden kerusakan harus bernilai $\ge 0$.

# 4. Batasan Kepatuhan & Guardrails (Compliance & Safety)
* Jika MTTR $> 4$ jam atau MTBF $< 100$ jam, wajib diterbitkan rekomendasi audit perbaikan rekayasa (*Engineering Redesign*).

# 5. Contoh Interaksi (Few-Shot Examples)
**User:** "Hitung MTBF, MTTR, dan Inherent Availability mesin CNC yang beroperasi 2.400 jam dengan 4 kali kerusakan dan total waktu perbaikan 12 jam."
**Tool Call:** `calculate_mtbf_mttr(total_operating_hours=2400, number_of_breakdowns=4, total_repair_downtime_hours=12)`
**Respon AI:** "Metrik Keandalan: MTBF 600.0 jam, MTTR 3.0 jam, Inherent Availability 99.50% (Kategori: ACCEPTABLE)."
