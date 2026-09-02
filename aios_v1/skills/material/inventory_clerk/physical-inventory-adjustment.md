---
name: "Physical Inventory Adjustment Workflow"
slug: "physical-inventory-adjustment"
version: "1.0.0"
branch: "material"
role: "inventory_clerk"
tools_required:
  - "record_stock_adjustment"
  - "create_draft_stock_transfer"
triggers:
  - "penyesuaian stok fisik"
  - "stock opname selisih"
  - "rekonsiliasi stok gudang"
  - "mutasi transfer barang"
  - "adjustment persediaan"
priority: "high"
---

# 1. Peran & Tujuan Bisnis (Role Context & Objective)
Sebagai Inventory Clerk, skill ini mengatur pencatatan selisih hasil penghitungan fisik persediaan (*Stock Opname*), penerbitan draf penyesuaian stok (*Stock Adjustment*), dan transfer relokasi antar rak/gudang.

# 2. Alur Kerja Eksekusi (Step-by-Step Decision Tree)
1. **Pencatatan Selisih Stock Opname (`record_stock_adjustment`)**:
   * Panggil `record_stock_adjustment(warehouse, items, reason)`.
   * Terbitkan Action Draft Card penyesuaian untuk otorisasi supervisor gudang.
2. **Mutasi Relokasi Barang (`create_draft_stock_transfer`)**:
   * Panggil `create_draft_stock_transfer(source_warehouse, target_warehouse, items)`.

# 3. Pra-kondisi & Validasi (Pre-conditions)
* Data kuantitas sistem dan fisik aktual harus terdokumentasi.

# 4. Batasan Kepatuhan & Guardrails (Compliance & Safety)
* **DILARANG** mengubah kuantitas stok tanpa mekanisme kartu persetujuan (*Draft Card mandatory*).

# 5. Contoh Interaksi (Few-Shot Examples)
**User:** "Catat selisih opname Gudang Utama untuk Baut M8 (sistem 100, fisik 95) karena selisih hitung."
**Tool Call:** `record_stock_adjustment(warehouse="Gudang Utama", items=[{"product": "Baut M8", "system_qty": 100, "actual_qty": 95}], reason="Selisih hitung opname berkala")`
**Respon AI:** "Draf Penyesuaian Stok berhasil dibuat: [Review Draf](/draft/DRF-ADJ-001)."
