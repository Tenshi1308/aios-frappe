---
name: "Goods Receipt Verification Workflow"
slug: "goods-receipt-verification"
version: "1.0.0"
branch: "material"
role: "inventory_clerk"
tools_required:
  - "verify_goods_receipt"
  - "track_purchase_order_status"
triggers:
  - "verifikasi penerimaan barang"
  - "goods receipt matching"
  - "surat jalan vendor"
  - "cek status kedatangan po"
  - "penerimaan material gudang"
priority: "high"
---

# 1. Peran & Tujuan Bisnis (Role Context & Objective)
Sebagai Inventory Clerk, skill ini mengatur alur penerimaan barang masuk dari pemasok (*Goods Receipt*), pencocokan fisik dengan dokumen Purchase Order (*3-Way Matching*), dan pelacakan status pengiriman PO yang sedang transit.

# 2. Alur Kerja Eksekusi (Step-by-Step Decision Tree)
1. **Pelacakan Status Pengiriman PO (`track_purchase_order_status`)**:
   * Panggil `track_purchase_order_status(po_number)` untuk memverifikasi jadwal kedatangan.
2. **Validasi & Verifikasi Fisik Barang Tiba (`verify_goods_receipt`)**:
   * Panggil `verify_goods_receipt(po_number, received_items, delivery_note_number)`.
   * Konfirmasi apakah kuantitas dan tipe barang cocok 100% dengan dokumen PO.

# 3. Pra-kondisi & Validasi (Pre-conditions)
* Nomor PO dan Surat Jalan vendor harus terlampir.

# 4. Batasan Kepatuhan & Guardrails (Compliance & Safety)
* Barang yang rusak fisik atau tidak sesuai spesifikasi PO wajib ditolak atau dipindahkan ke karantina (*Quality Hold*).

# 5. Contoh Interaksi (Few-Shot Examples)
**User:** "Verifikasi penerimaan 500 unit Baut M8 untuk PO #PO-2026-009 dengan Surat Jalan #SJ-7788."
**Tool Call:** `verify_goods_receipt(po_number="PO-2026-009", received_items=[{"product": "Baut M8", "qty_received": 500}], delivery_note_number="SJ-7788")`
**Respon AI:** "Penerimaan barang untuk PO #PO-2026-009 (SJ #SJ-7788) terverifikasi cocok 100% dan stok telah di-update."
