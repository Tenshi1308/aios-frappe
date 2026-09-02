---
name: "Measurement Recording and Calibration Workflow"
slug: "measurement-recording-and-calibration"
version: "1.0.0"
branch: "quality"
role: "quality_inspector"
tools_required:
  - "record_inspection_results"
  - "verify_calibration_status"
triggers:
  - "catat hasil ukur qc"
  - "cek kalibrasi alat ukur"
  - "pengukuran dimensi sampel lab"
  - "uji fisik ketebalan"
  - "verifikasi masa kalibrasi micrometer"
priority: "high"
---

# 1. Peran & Tujuan Bisnis (Role Context & Objective)
Sebagai Quality Inspector, skill ini mengatur verifikasi keabsahan sertifikat kalibrasi alat ukur laboratorium presisi (Micrometer, Vernier Caliper, Tensile Tester) sebelum digunakan, serta pencatatan resmi hasil pengukuran parameter fisik/dimensi sampel uji laboratorium.

# 2. Alur Kerja Eksekusi (Step-by-Step Decision Tree)
1. **Verifikasi Masa Berlaku Kalibrasi Alat Ukur (`verify_calibration_status`)**:
   * Panggil `verify_calibration_status(equipment_id, equipment_name)`.
   * Pastikan alat berstatus VALID (`is_safe_to_use = True`).
2. **Pencatatan Hasil Pengukuran Parameter Uji (`record_inspection_results`)**:
   * Panggil `record_inspection_results(lot_id, measured_values, sample_size, is_within_spec)`.
   * Dapatkan status kesesuaian: CONFORMING (PASS) atau NON_CONFORMING (FAIL).

# 3. Pra-kondisi & Validasi (Pre-conditions)
* Alat ukur yang kedaluwarsa masa kalibrasinya dilarang digunakan untuk pengujian resmi.

# 4. Batasan Kepatuhan & Guardrails (Compliance & Safety)
* Data ukur tidak boleh dimanipulasi atau dibulatkan di luar batas toleransi instrumen.

# 5. Contoh Interaksi (Few-Shot Examples)
**User:** "Cek status kalibrasi Micrometer Mitutoyo #MIC-01 dan catat hasil uji ketebalan 30 sampel pada Lot LOT-089 (seluruh sampel 3.01mm memenuhi spek)."
**Tool Call:** `verify_calibration_status(equipment_id="MIC-01", equipment_name="Digital Micrometer Mitutoyo")`
**Tool Call:** `record_inspection_results(lot_id="LOT-089", measured_values=[{"param": "Ketebalan", "value": 3.01, "spec": "3.0 +/- 0.05"}], sample_size=30, is_within_spec=True)`
**Respon AI:** "Kalibrasi Micrometer aktif hingga 15 Maret 2027. Hasil uji 30 sampel Lot #LOT-089 tercatat CONFORMING (PASS)."
