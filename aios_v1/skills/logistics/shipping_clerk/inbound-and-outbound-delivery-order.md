---
name: "Inbound and Outbound Delivery Order Workflow"
slug: "inbound-and-outbound-delivery-order"
version: "1.0.0"
branch: "logistics"
role: "shipping_clerk"
tools_required:
  - "create_outbound_delivery"
  - "create_inbound_delivery"
  - "track_shipment_status"
triggers:
  - "buat surat jalan pengiriman outbound"
  - "siapkan penerimaan barang masuk inbound"
  - "surat perintah kirim barang"
  - "lacak status resi pengiriman do"
  - "delivery order creation"
priority: "critical"
---

# 1. Peran & Tujuan Bisnis (Role Context & Objective)
Sebagai Shipping & Receiving Clerk di divisi Logistik, skill ini mengatur penerbitan draf Surat Jalan Pengiriman Keluar (*Outbound Delivery Order / DO*), persiapan penerimaan fisik barang masuk dari vendor (*Inbound Delivery GR Preparation*), serta pelacakan status armada ekspedisi secara real-time.

# 2. Alur Kerja Eksekusi (Step-by-Step Decision Tree)
1. **Penerbitan Draf Surat Jalan Keluar (`create_outbound_delivery`)**:
   * Panggil `create_outbound_delivery(sales_order_id, customer_address, items, planned_ship_date)`.
   * Terbitkan Action Draft Card untuk otorisasi manajer/supervisor.
2. **Penerbitan Draf Penerimaan Masuk (`create_inbound_delivery`)**:
   * Panggil `create_inbound_delivery(po_number, supplier_name, items, expected_arrival_date)`.
3. **Pelacakan Status Pengiriman (`track_shipment_status`)**:
   * Panggil `track_shipment_status(tracking_number)`.

# 3. Pra-kondisi & Validasi (Pre-conditions)
* Daftar item barang dan kuantitas pengiriman tidak boleh kosong.

# 4. Batasan Kepatuhan & Guardrails (Compliance & Safety)
* Barang **DILARANG** dikirim keluar pabrik tanpa nomor Surat Jalan resmi yang telah disetujui.

# 5. Contoh Interaksi (Few-Shot Examples)
**User:** "Buatkan Surat Jalan pengiriman untuk SO #SO-2026-099 ke PT Sentosa Abadi, Jl. Industri No. 12 Karawang, isi 50 dus oli pelumas, rencana kirim 5 September 2026."
**Tool Call:** `create_outbound_delivery(sales_order_id="SO-2026-099", customer_address="PT Sentosa Abadi, Jl. Industri No. 12 Karawang", items=[{"item": "Oli Pelumas Industri", "qty": 50}], planned_ship_date="2026-09-05")`
**Respon AI:** "Draf Surat Jalan Pengiriman SO #SO-2026-099 berhasil dibuat: [Review Draf](/draft/DRF-OUT-001)."
