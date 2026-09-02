---
name: "Work Hours and Parts Consumption Workflow"
slug: "work-hours-and-parts-consumption"
version: "1.0.0"
branch: "maintenance"
role: "maintenance_technician"
tools_required:
  - "log_technician_work_hours"
  - "track_spare_parts_usage"
triggers:
  - "catat jam kerja teknisi wo"
  - "catat pemakaian spare parts servis"
  - "konsumsi suku cadang perbaikan mesin"
  - "lapor jam pengerjaan maintenance"
  - "technician work logging"
priority: "high"
---

# 1. Peran & Tujuan Bisnis (Role Context & Objective)
Sebagai Maintenance Technician, skill ini mengatur pencatatan jam kerja aktual perbaikan mesin pada nomor *Work Order* terkait, serta pencatatan pemakaian suku cadang (*Spare Parts Consumption*) guna penghitungan biaya pemeliharaan mesin yang akurat.

# 2. Alur Kerja Eksekusi (Step-by-Step Decision Tree)
1. **Pencatatan Jam Kerja Teknisi (`log_technician_work_hours`)**:
   * Panggil `log_technician_work_hours(work_order_id, technician_name, hours_spent, task_summary)`.
2. **Pencatatan Pemakaian Suku Cadang Mesin (`track_spare_parts_usage`)**:
   * Panggil `track_spare_parts_usage(work_order_id, parts_used)`.
   * Hitung total biaya material suku cadang yang digunakan.

# 3. Pra-kondisi & Validasi (Pre-conditions)
* Jam kerja yang dicatat tidak boleh bernilai $\le 0$.

# 4. Batasan Kepatuhan & Guardrails (Compliance & Safety)
* Seluruh suku cadang yang keluar dari gudang wajib ditautkan ke nomor Work Order resmi.

# 5. Contoh Interaksi (Few-Shot Examples)
**User:** "Catat pengerjaan 3.5 jam oleh Teknisi Agus pada WO-202 dan pemakaian 2 unit Bearing 6205 (@ Rp 150.000)."
**Tool Call:** `log_technician_work_hours(work_order_id="WO-202", technician_name="Agus Setiawan", hours_spent=3.5, task_summary="Penggantian bearing spindle utama")`
**Tool Call:** `track_spare_parts_usage(work_order_id="WO-202", parts_used=[{"part_no": "BEARING-6205", "qty": 2, "unit_cost": 150000}])`
**Respon AI:** "Jam kerja Agus (3.5 jam) dan pemakaian 2 unit Bearing 6205 (Rp 300.000) untuk WO #WO-202 berhasil dicatat."
