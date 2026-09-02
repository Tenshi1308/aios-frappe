---
name: "Shop Floor Output and Scrap Logging Workflow"
slug: "shop-floor-output-and-scrap-logging"
version: "1.0.0"
branch: "manufacturing"
role: "production_supervisor"
tools_required:
  - "confirm_production_output"
  - "report_production_scrap"
  - "track_work_order_progress"
triggers:
  - "konfirmasi output produksi selesai"
  - "catat barang reject scrap pabrik"
  - "lapor limbah produksi"
  - "progres pekerjaan lantai pabrik"
  - "shop floor confirmation"
priority: "high"
---

# 1. Peran & Tujuan Bisnis (Role Context & Objective)
Sebagai Production Supervisor di lantai pabrik (*Shop Floor*), skill ini mengatur pelaporan konfirmasi hasil jadi barang yang selesai diproses (*Production Output Confirmation*), pencatatan barang cacat/limbah sisa (*Scrap & Reject Logging*), serta pemantauan status pekerjaan stasiun perakitan secara langsung.

# 2. Alur Kerja Eksekusi (Step-by-Step Decision Tree)
1. **Pemantauan Status Progres Pekerjaan (`track_work_order_progress`)**:
   * Panggil `track_work_order_progress(production_order_id)`.
2. **Konfirmasi Hasil Output Barang Jadi (`confirm_production_output`)**:
   * Panggil `confirm_production_output(production_order_id, completed_quantity, operator_name)`.
   * Terbitkan Action Draft Card untuk otorisasi supervisor/manajer.
3. **Pencatatan Limbah & Produk Reject (`report_production_scrap`)**:
   * Panggil `report_production_scrap(production_order_id, scrap_quantity, scrap_reason, material_id)`.

# 3. Pra-kondisi & Validasi (Pre-conditions)
* Kuantitas konfirmasi output dan scrap tidak boleh melebihi target order.

# 4. Batasan Kepatuhan & Guardrails (Compliance & Safety)
* Seluruh barang scrap wajib disertai alasan kerusakan teknis yang jelas.

# 5. Contoh Interaksi (Few-Shot Examples)
**User:** "Konfirmasi penyelesaian 40 unit barang jadi pada MO-001 oleh operator Budi Santoso."
**Tool Call:** `confirm_production_output(production_order_id="MO-001", completed_quantity=40, operator_name="Budi Santoso")`
**Respon AI:** "Draf Konfirmasi Output MO #MO-001 (40 unit) berhasil dibuat dan siap di-approve: [Review Draf](/draft/DRF-OUTPUT-001)."
