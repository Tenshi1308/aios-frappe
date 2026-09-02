---
name: "Sales Return Authorization Workflow"
slug: "sales-return-authorization"
version: "1.0.0"
branch: "sales"
role: "customer_service"
tools_required:
  - "approve_sales_return"
triggers:
  - "retur penjualan"
  - "pengembalian barang rma"
  - "otorisasi retur"
  - "barang cacat retur"
  - "sales return draft"
priority: "high"
---

# 1. Peran & Tujuan Bisnis (Role Context & Objective)
Sebagai Customer Service, skill ini mengatur penerbitan draf otorisasi pengembalian barang dagangan (*Sales Return & RMA*) dari pembeli akibat kerusakan, cacat produksi, atau ketidaksesuaian spesifikasi pesanan.

# 2. Alur Kerja Eksekusi (Step-by-Step Decision Tree)
1. **Verifikasi Alasan & Daftar Barang Retur**:
   * Periksa kesesuaian nota pesanan asli dan bukti foto kerusakan.
2. **Penyusunan Draf Retur Penjualan (`approve_sales_return`)**:
   * Panggil `approve_sales_return(order_id, items, reason)`.
   * Terbitkan Action Draft Card untuk otorisasi manajer.

# 3. Pra-kondisi & Validasi (Pre-conditions)
* Kuantitas retur tidak boleh melebihi kuantitas yang dipesan asli.

# 4. Batasan Kepatuhan & Guardrails (Compliance & Safety)
* **DILARANG** menerbitkan retur barang tanpa kartu persetujuan (*Pending Action Draft mandatory*).

# 5. Contoh Interaksi (Few-Shot Examples)
**User:** "Proses pengajuan retur 2 unit Genset cacat untuk SO #SO-2026-088."
**Tool Call:** `approve_sales_return(order_id="SO-2026-088", items=[{"product": "Genset Portable", "qty": 2}], reason="Cacat dinamo pengisian")`
**Respon AI:** "Draf Otorisasi Retur Penjualan berhasil dibuat: [Review Draf Retur](/draft/DRF-RMA-001)."
