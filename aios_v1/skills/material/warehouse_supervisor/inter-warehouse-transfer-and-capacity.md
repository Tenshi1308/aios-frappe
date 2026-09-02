---
name: "Inter-Warehouse Transfer and Capacity Workflow"
slug: "inter-warehouse-transfer-and-capacity"
version: "1.0.0"
branch: "material"
role: "warehouse_supervisor"
tools_required:
  - "create_draft_stock_transfer"
  - "get_warehouse_capacity_utilization"
triggers:
  - "mutasi antar gudang"
  - "transfer stok gudang"
  - "kapasitas palet gudang"
  - "utilisasi ruang simpan"
  - "relokasi stok persediaan"
priority: "high"
---

# 1. Peran & Tujuan Bisnis (Role Context & Objective)
Sebagai Warehouse Supervisor, skill ini mengatur perancangan dan otorisasi draf mutasi persediaan antar gudang (*Inter-Warehouse Transfer*), serta pemantauan persentase utilisasi kapasitas ruang penyimpanan palet di setiap fasilitas gudang.

# 2. Alur Kerja Eksekusi (Step-by-Step Decision Tree)
1. **Pemantauan Kapasitas Gudang Tujuan (`get_warehouse_capacity_utilization`)**:
   * Panggil `get_warehouse_capacity_utilization(warehouse_name)`.
   * Pastikan gudang tujuan memiliki ruang kosong yang memadai (< 85% terpakai).
2. **Pembuatan Draf Mutasi Antar Gudang (`create_draft_stock_transfer`)**:
   * Panggil `create_draft_stock_transfer(source_warehouse, target_warehouse, items)`.
   * Terbitkan Action Draft Card untuk otorisasi pemindahan fisik barang.

# 3. Pra-kondisi & Validasi (Pre-conditions)
* Gudang asal dan gudang tujuan harus aktif di master fasilitas.

# 4. Batasan Kepatuhan & Guardrails (Compliance & Safety)
* **DILARANG** melakukan mutasi barang ke gudang yang telah mencapai kapasitas maksimal (> 95%).

# 5. Contoh Interaksi (Few-Shot Examples)
**User:** "Tolong periksa kapasitas Gudang Cabang Surabaya dan buatkan draf mutasi 200 unit Baut M8 dari Gudang Utama."
**Tool Call:** `get_warehouse_capacity_utilization(warehouse_name="Gudang Surabaya")`
**Tool Call:** `create_draft_stock_transfer(source_warehouse="Gudang Utama", target_warehouse="Gudang Surabaya", items=[{"product": "Baut M8", "qty": 200}])`
**Respon AI:** "Utilisasi Gudang Surabaya adalah 71.6% (Optimal). Draf Transfer Stok berhasil dibuat: [Review Draf](/draft/DRF-STR-001)."
