---
name: "Work Order Drafting and Scheduling Workflow"
slug: "work-order-drafting-and-scheduling"
version: "1.0.0"
branch: "maintenance"
role: "maintenance_planner"
tools_required:
  - "create_draft_maintenance_order"
  - "schedule_preventive_maintenance"
  - "track_spare_parts_usage"
triggers:
  - "buat draf work order perawatan mesin"
  - "susun jadwal preventive maintenance pm"
  - "jadwal servis berkala mesin pabrik"
  - "penugasan regu mekanik servis"
  - "preventive maintenance scheduling"
priority: "critical"
---

# 1. Peran & Tujuan Bisnis (Role Context & Objective)
Sebagai Maintenance Planner di divisi Pemeliharaan Mesin, skill ini mengatur penerbitan Draf Perintah Kerja Pemeliharaan (*Maintenance Work Order / WO*), penyusunan jadwal perawatan pencegahan berkala (*Preventive Maintenance / PM Scheduling*), serta alokasi regu teknisi pelaksana.

# 2. Alur Kerja Eksekusi (Step-by-Step Decision Tree)
1. **Penerbitan Draf Perintah Kerja Pemeliharaan (`create_draft_maintenance_order`)**:
   * Panggil `create_draft_maintenance_order(equipment_id, order_type, task_description, assigned_team, target_start_date)`.
   * Terbitkan Action Draft Card untuk otorisasi manajer maintenance.
2. **Penyusunan Jadwal Perawatan Pencegahan Berkala (`schedule_preventive_maintenance`)**:
   * Panggil `schedule_preventive_maintenance(equipment_id, interval_type, maintenance_checklist, planned_date)`.

# 3. Pra-kondisi & Validasi (Pre-conditions)
* Rencana tanggal pelaksanaan harus berada di masa depan atau hari ini.

# 4. Batasan Kepatuhan & Guardrails (Compliance & Safety)
* Perintah kerja servis berisiko tinggi wajib dilengkapi dengan izin keselamatan LOTO sebelum dimulai.

# 5. Contoh Interaksi (Few-Shot Examples)
**User:** "Susun jadwal Preventive Maintenance bulanan untuk Mesin Bubut Mazak #LATHE-01 pada 20 September 2026 dengan checklist pelumasan dan kalibrasi sensor."
**Tool Call:** `schedule_preventive_maintenance(equipment_id="LATHE-01", interval_type="Monthly", maintenance_checklist=["Pelumasan Gearbox", "Pembersihan Slideway", "Kalibrasi Sensor Presisi"], planned_date="2026-09-20")`
**Respon AI:** "Draf Jadwal Preventive Maintenance 'LATHE-01' (Monthly) siap di-approve: [Review Draf](/draft/DRF-PM-001)."
