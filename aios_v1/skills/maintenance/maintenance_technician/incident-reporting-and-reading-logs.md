---
name: "Incident Reporting and Reading Logs Workflow"
slug: "incident-reporting-and-reading-logs"
version: "1.0.0"
branch: "maintenance"
role: "maintenance_technician"
tools_required:
  - "create_maintenance_request"
  - "log_equipment_reading"
triggers:
  - "lapor kerusakan mesin pabrik"
  - "catat parameter sensor suhu vibrasi"
  - "permintaan servis perbaikan mesin"
  - "inspeksi kondisi harian mesin"
  - "maintenance incident reading"
priority: "high"
---

# 1. Peran & Tujuan Bisnis (Role Context & Objective)
Sebagai Maintenance Technician di lini pabrik, skill ini mengatur penerbitan draf laporan kerusakan mesin / permintaan servis perbaikan (*Maintenance Request*), serta pencatatan rutin parameter kesehatan mesin real-time (Suhu Bearing, Getaran Vibrasi RMS, Tekanan Hidrolik, dan Hour Meter).

# 2. Alur Kerja Eksekusi (Step-by-Step Decision Tree)
1. **Pencatatan Parameter Kesehatan Fisik Mesin (`log_equipment_reading`)**:
   * Panggil `log_equipment_reading(equipment_id, temperature_c, vibration_mms, operating_hours, pressure_bar)`.
   * Evaluasi status: NORMAL ($T \le 75^\circ\text{C}, V \le 4.5\text{ mm/s}$) atau WARNING.
2. **Penerbitan Draf Permintaan Perbaikan Mesin (`create_maintenance_request`)**:
   * Jika mesin mogok atau terdeteksi anomali kritis, panggil `create_maintenance_request(equipment_id, issue_description, priority, reporter_name)`.
   * Terbitkan Action Draft Card untuk disposisi supervisor maintenance.

# 3. Pra-kondisi & Validasi (Pre-conditions)
* Parameter suhu dan vibrasi harus bernilai numerik non-negatif.

# 4. Batasan Kepatuhan & Guardrails (Compliance & Safety)
* Kerusakan dengan potensi bahaya keselamatan kerja wajib diberi prioritas `Emergency`.

# 5. Contoh Interaksi (Few-Shot Examples)
**User:** "Catat reading Mesin CNC Milling CNC-01 (suhu 82C, vibrasi 5.2 mm/s, hour meter 4.200 jam) dan buatkan request perbaikan darurat."
**Tool Call:** `log_equipment_reading(equipment_id="CNC-01", temperature_c=82.0, vibration_mms=5.2, operating_hours=4200)`
**Tool Call:** `create_maintenance_request(equipment_id="CNC-01", issue_description="Overheating bearing spindle dan getaran abnormal tinggi", priority="Emergency", reporter_name="Teknisi Budi")`
**Respon AI:** "Reading CNC-01 tercatat POTENSI ANOMALI (82°C & 5.2 mm/s). Draf Permintaan Servis Darurat berhasil dibuat: [Review Draf](/draft/DRF-REQ-001)."
