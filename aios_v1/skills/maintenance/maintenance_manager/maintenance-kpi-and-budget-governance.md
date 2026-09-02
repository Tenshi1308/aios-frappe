---
name: "Maintenance KPI and Budget Governance Workflow"
slug: "maintenance-kpi-and-budget-governance"
version: "1.0.0"
branch: "maintenance"
role: "maintenance_manager"
tools_required:
  - "report_maintenance_kpi_summary"
  - "estimate_maintenance_cost"
  - "calculate_overall_equipment_availability"
triggers:
  - "laporan kpi pemeliharaan mesin"
  - "ketersediaan mesin uptime availability"
  - "rasio planned vs unplanned maintenance"
  - "tata kelola anggaran biaya pemeliharaan"
  - "maintenance governance kpi"
priority: "critical"
---

# 1. Peran & Tujuan Bisnis (Role Context & Objective)
Sebagai Maintenance Manager di divisi Plant Maintenance, skill ini mengatur kepemimpinan tata kelola pemeliharaan aset pabrik (*Maintenance Governance*), evaluasi pencapaian Key Performance Indicators (*KPI: Planned vs Unplanned Maintenance Ratio, Work Order Completion Rate*), pengendalian anggaran biaya servis, serta penghitungan ketersediaan mesin siap operasi (*Operational Uptime Availability*).

# 2. Alur Kerja Eksekusi (Step-by-Step Decision Tree)
1. **Evaluasi Metrik KPI Bulanan Divisi Maintenance (`report_maintenance_kpi_summary`)**:
   * Panggil `report_maintenance_kpi_summary(period_month)`.
   * Evaluasi rasio Planned Maintenance terhadap target ($\ge 80\%$).
2. **Kalkulasi Ketersediaan Mesin Siap Operasi (`calculate_overall_equipment_availability`)**:
   * Panggil `calculate_overall_equipment_availability(total_calendar_hours, unplanned_downtime_hours, planned_maintenance_hours)`.
3. **Pengendalian Anggaran Biaya Servis (`estimate_maintenance_cost`)**:
   * Evaluasi alokasi biaya tenaga kerja teknisi dan suku cadang.

# 3. Pra-kondisi & Validasi (Pre-conditions)
* Rekonsiliasi seluruh Work Order bulan berjalan harus selesai sebelum penutupan laporan KPI.

# 4. Batasan Kepatuhan & Guardrails (Compliance & Safety)
* Jika rasio *Unplanned Corrective Maintenance* $> 30\%$, manajer wajib mengadakan rapat audit keandalan pabrik.

# 5. Contoh Interaksi (Few-Shot Examples)
**User:** "Tampilkan ringkasan KPI Maintenance bulan ini dan hitung ketersediaan mesin jika dari 720 jam kalender, terdapat 24 jam downtime tak terencana dan 16 jam perawatan terencana."
**Tool Call:** `report_maintenance_kpi_summary(period_month="Current Month")`
**Tool Call:** `calculate_overall_equipment_availability(total_calendar_hours=720, unplanned_downtime_hours=24, planned_maintenance_hours=16)`
**Respon AI:** "KPI Maintenance: Completion 96.5%, Planned Ratio 82.0%. Ketersediaan Mesin Operasional: 94.4% (680/720 jam operasi)."
