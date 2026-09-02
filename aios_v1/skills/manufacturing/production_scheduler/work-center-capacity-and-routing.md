---
name: "Work Center Capacity and Routing Workflow"
slug: "work-center-capacity-and-routing"
version: "1.0.0"
branch: "manufacturing"
role: "production_scheduler"
tools_required:
  - "check_work_center_capacity"
  - "manage_routing_workstations"
triggers:
  - "kapasitas stasiun kerja mesin"
  - "work center capacity load"
  - "konfigurasi routing operasi"
  - "alokasi beban mesin pabrik"
  - "urutan stasiun kerja lini produksi"
priority: "high"
---

# 1. Peran & Tujuan Bisnis (Role Context & Objective)
Sebagai Production Scheduler, skill ini mengatur evaluasi kapasitas mesin/stasiun kerja pabrik (*Work Center Capacity Utilization*) untuk mencegah kelebihan beban (*Overload Bottleneck*) serta penyusunan urutan stasiun kerja (*Routing Configuration*) proses perakitan barang.

# 2. Alur Kerja Eksekusi (Step-by-Step Decision Tree)
1. **Evaluasi Utilisasi Kapasitas Mesin (`check_work_center_capacity`)**:
   * Panggil `check_work_center_capacity(work_center_id, target_week)`.
   * Evaluasi beban: NORMAL ($\le 85\%$) atau OVERLOAD_RISK ($> 85\%$).
2. **Penyusunan Routing Operasi Mesin (`manage_routing_workstations`)**:
   * Panggil `manage_routing_workstations(product_id, operations)`.
   * Terbitkan Action Draft Card untuk otorisasi konfigurasi routing.

# 3. Pra-kondisi & Validasi (Pre-conditions)
* Work center dan mesin harus terdaftar dalam kondisi aktif / tidak berstatus breakdown.

# 4. Batasan Kepatuhan & Guardrails (Compliance & Safety)
* **DILARANG** mengalokasikan pekerjaan baru pada work center yang telah berstatus *Overload Risk* tanpa persetujuan manajer pabrik.

# 5. Contoh Interaksi (Few-Shot Examples)
**User:** "Cek kapasitas mesin di Lini Mesin CNC untuk minggu ini."
**Tool Call:** `check_work_center_capacity(work_center_id="Lini Mesin CNC", target_week="Minggu Ke-36")`
**Respon AI:** "Kapasitas Lini Mesin CNC: Utilisasi 78.1% (62.5/80 jam terpakai) berstatus NORMAL."
