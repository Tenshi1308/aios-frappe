---
name: "Warehouse Goods Movement and POD Workflow"
slug: "warehouse-goods-movement-and-pod"
version: "1.0.0"
branch: "logistics"
role: "shipping_clerk"
tools_required:
  - "confirm_goods_receipt"
  - "confirm_goods_issue"
  - "log_pod_proof_of_delivery"
triggers:
  - "konfirmasi penerimaan fisik barang gudang"
  - "konfirmasi barang keluar dermaga"
  - "catat bukti tanda terima pod"
  - "upload bukti serah terima kiriman"
  - "proof of delivery logging"
priority: "high"
---

# 1. Peran & Tujuan Bisnis (Role Context & Objective)
Sebagai Shipping & Receiving Clerk di dermaga gudang (*Loading Dock*), skill ini mengatur konfirmasi fisik barang tiba di gudang logistik (*Goods Receipt Confirmation*), validasi pelepasan barang ke truk (*Goods Issue Validation*), serta pencatatan resmi tanda terima barang bertandatangan (*Proof of Delivery / POD*).

# 2. Alur Kerja Eksekusi (Step-by-Step Decision Tree)
1. **Konfirmasi Fisik Barang Masuk (`confirm_goods_receipt`)**:
   * Panggil `confirm_goods_receipt(delivery_id, received_items, receiver_name)`.
2. **Konfirmasi Pelepasan Barang ke Armada (`confirm_goods_issue`)**:
   * Panggil `confirm_goods_issue(delivery_id, issued_items, picker_name)`.
3. **Pencatatan Bukti Serah Terima Pelanggan (`log_pod_proof_of_delivery`)**:
   * Panggil `log_pod_proof_of_delivery(delivery_id, recipient_name, received_timestamp, pod_signature_ref)`.

# 3. Pra-kondisi & Validasi (Pre-conditions)
* Kuantitas yang dikonfirmasi harus sesuai dengan hasil hitung fisik di dermaga.

# 4. Batasan Kepatuhan & Guardrails (Compliance & Safety)
* Status pengiriman tidak boleh ditutup sebelum bukti POD fisik/digital terunggah.

# 5. Contoh Interaksi (Few-Shot Examples)
**User:** "Catat bukti penerimaan barang POD untuk DO #DO-8890 yang diterima oleh Bapak Slamet pada 2 September 2026 jam 14:00 (Ref TTD: IMG-POD-8890.jpg)."
**Tool Call:** `log_pod_proof_of_delivery(delivery_id="DO-8890", recipient_name="Bapak Slamet", received_timestamp="2026-09-02 14:00", pod_signature_ref="IMG-POD-8890.jpg")`
**Respon AI:** "Draf Rekam POD #DO-8890 (Penerima: Bapak Slamet) siap di-approve: [Review Draf](/draft/DRF-POD-001)."
