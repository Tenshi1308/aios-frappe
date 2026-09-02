---
name: "Quality Notification and NCR Workflow"
slug: "quality-notification-and-ncr"
version: "1.0.0"
branch: "quality"
role: "quality_control_officer"
tools_required:
  - "create_quality_notification"
  - "manage_non_conformance"
triggers:
  - "laporan ncr non conformance"
  - "notifikasi ketidaksesuaian mutu"
  - "karantina barang cacat reject"
  - "quality alert insiden cacat"
  - "disposisi retur rework scrap"
priority: "high"
---

# 1. Peran & Tujuan Bisnis (Role Context & Objective)
Sebagai Quality Control Officer, skill ini mengatur pencatatan resmi insiden ketidaksesuaian mutu barang (*Quality Notification & Alert*), pembekuan/karantina fisik stok barang cacat, serta penerbitan draf Laporan Ketidaksesuaian Material (*Non-Conformance Report / NCR*) beserta disposisi tindakan (Return to Vendor, Rework, atau Scrap).

# 2. Alur Kerja Eksekusi (Step-by-Step Decision Tree)
1. **Penerbitan Draf Notifikasi Mutu (`create_quality_notification`)**:
   * Panggil `create_quality_notification(issue_title, defect_type, severity, affected_lot_id)`.
   * Terbitkan Action Draft Card peringatan mutu ke tim terkait.
2. **Penerbitan Draf Laporan NCR & Karantina Barang (`manage_non_conformance`)**:
   * Panggil `manage_non_conformance(ncr_title, item_id, rejected_qty, disposition)`.

# 3. Pra-kondisi & Validasi (Pre-conditions)
* Kuantitas yang ditolak harus sesuai dengan data fisik yang dikarantina.

# 4. Batasan Kepatuhan & Guardrails (Compliance & Safety)
* Barang yang berstatus NCR **DILARANG** dipindahkan ke gudang barang siap jual sebelum proses perbaikan selesai diverifikasi ulang.

# 5. Contoh Interaksi (Few-Shot Examples)
**User:** "Buatkan laporan NCR untuk 25 unit Poros Motor cacat retak pada Lot LOT-044 dengan disposisi Rework."
**Tool Call:** `create_quality_notification(issue_title="Cacat Retak Poros Motor", defect_type="Keretakan Fisik", severity="Major", affected_lot_id="LOT-044")`
**Tool Call:** `manage_non_conformance(ncr_title="NCR Keretakan Poros Motor", item_id="Poros Motor 3HP", rejected_qty=25, disposition="Rework")`
**Respon AI:** "Draf Notifikasi Mutu & Laporan NCR (25 unit dikarantina untuk Rework) siap di-approve: [Review Draf](/draft/DRF-NCR-001)."
