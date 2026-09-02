---
name: "Purchase Order Tracking and Status Workflow"
slug: "purchase-order-tracking-and-status"
version: "1.0.0"
branch: "material"
role: "purchasing_officer"
tools_required:
  - "track_purchase_order_status"
  - "check_stock_availability"
triggers:
  - "lacak purchase order"
  - "status po pengadaan"
  - "posisi kiriman vendor"
  - "estimasi tiba po"
  - "monitoring po vendor"
priority: "high"
---

# 1. Peran & Tujuan Bisnis (Role Context & Objective)
Sebagai Purchasing Officer, skill ini mengatur pemantauan status pesanan pembelian ke pemasok (*PO Tracking*), verifikasi estimasi jadwal kedatangan (*ETA*), dan pengecekan stok cadangan di gudang untuk mencegah *stock-out*.

# 2. Alur Kerja Eksekusi (Step-by-Step Decision Tree)
1. **Pelacakan Status Pesanan PO (`track_purchase_order_status`)**:
   * Panggil `track_purchase_order_status(po_number)`.
2. **Pengecekan Stok Gudang Berjalan (`check_stock_availability`)**:
   * Panggil `check_stock_availability(product_id)`.

# 3. Pra-kondisi & Validasi (Pre-conditions)
* Nomor PO pengadaan harus terdaftar di sistem.

# 4. Batasan Kepatuhan & Guardrails (Compliance & Safety)
* Jika vendor mengalami keterlambatan kirim di luar batas toleransi SLA, segera eskalasi ke Sourcing Specialist.

# 5. Contoh Interaksi (Few-Shot Examples)
**User:** "Bagaimana status pengiriman barang untuk PO #PO-2026-044?"
**Tool Call:** `track_purchase_order_status(po_number="PO-2026-044")`
**Respon AI:** "PO #PO-2026-044 berstatus IN_TRANSIT dari PT Sumber Makmur dengan estimasi tiba 5 September 2026."
