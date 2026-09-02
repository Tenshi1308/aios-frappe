---
name: "Predictive Maintenance and RCM Workflow"
slug: "predictive-maintenance-and-rcm"
version: "1.0.0"
branch: "maintenance"
role: "reliability_engineer"
tools_required:
  - "predict_equipment_failure"
  - "run_rcm_analysis"
triggers:
  - "prediksi kerusakan dini mesin pdm"
  - "analisis rcm reliability centered maintenance"
  - "strategi perawatan berbasis kondisi"
  - "deteksi anomali getaran suhu mesin"
  - "predictive maintenance rcm"
priority: "high"
---

# 1. Peran & Tujuan Bisnis (Role Context & Objective)
Sebagai Reliability Engineer, skill ini mengatur perancangan strategi pemeliharaan berbasis keandalan (*Reliability Centered Maintenance / RCM*) untuk setiap jenis aset kritis, serta deteksi dini potensi kerusakan mesin (*Predictive Maintenance / PdM*) menggunakan deviasi data tren sensor getaran dan temperatur sebelum terjadi kegagalan fatal (*Catastrophic Breakdown*).

# 2. Alur Kerja Eksekusi (Step-by-Step Decision Tree)
1. **Analisis Strategi Pemeliharaan Optimal RCM (`run_rcm_analysis`)**:
   * Panggil `run_rcm_analysis(equipment_id, failure_mode, failure_consequence, is_safety_critical)`.
2. **Prediksi Potensi Kerusakan Dini PdM (`predict_equipment_failure`)**:
   * Panggil `predict_equipment_failure(equipment_id, current_temp_c, current_vibration_mms, normal_max_temp, normal_max_vibration)`.
   * Dapatkan status sisa umur operasional (*Health State*) dan rekomendasi tindakan darurat/terencana.

# 3. Pra-kondisi & Validasi (Pre-conditions)
* Parameter pembacaan sensor harus valid dan terhubung dengan sistem IoT pabrik.

# 4. Batasan Kepatuhan & Guardrails (Compliance & Safety)
* Jika hasil prediksi menunjukkan `CRITICAL_FAILURE_IMMINENT`, mesin wajib segera diisolasi dan dihentikan dalam waktu maksimal 2 jam.

# 5. Contoh Interaksi (Few-Shot Examples)
**User:** "Analisis prediksi kesehatan Motor Pompa PUMP-03 dengan suhu aktual 88C (standar maks 75C) dan vibrasi 6.5 mm/s (standar maks 4.5 mm/s)."
**Tool Call:** `predict_equipment_failure(equipment_id="PUMP-03", current_temp_c=88.0, current_vibration_mms=6.5, normal_max_temp=75.0, normal_max_vibration=4.5)`
**Respon AI:** "Prediksi Pemeliharaan #PUMP-03: CRITICAL_FAILURE_IMMINENT (Sisa umur: 24-48 jam). Tindakan: Hentikan mesin segera dan lakukan inspeksi bearing darurat."
