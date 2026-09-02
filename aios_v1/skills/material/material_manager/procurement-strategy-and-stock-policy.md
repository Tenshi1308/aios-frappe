---
name: "Procurement Strategy and Stock Policy Governance Workflow"
slug: "procurement-strategy-and-stock-policy"
version: "1.0.0"
branch: "material"
role: "material_manager"
tools_required:
  - "check_stock_availability"
  - "evaluate_vendor_performance"
  - "get_warehouse_capacity_utilization"
triggers:
  - "kebijakan pengadaan material"
  - "tata kelola logistik gudang"
  - "strategi sourcing material"
  - "evaluasi manajer pengadaan"
  - "kebijakan persediaan korporat"
priority: "critical"
---

# 1. Peran & Tujuan Bisnis (Role Context & Objective)
Sebagai Material Manager, skill ini mengatur tata kelola strategis pengadaan material dan persediaan di seluruh pabrik/gudang perusahaan, evaluasi keandalan rantai pasok vendor, dan pengawasan kapasitas fasilitas logistik.

# 2. Alur Kerja Eksekusi (Step-by-Step Decision Tree)
1. **Pengawasan Kapasitas Logistik & Ketersediaan Stok**:
   * Panggil `check_stock_availability(...)` dan `get_warehouse_capacity_utilization(...)`.
2. **Evaluasi Kebijakan Vendor & Rantai Pasok**:
   * Panggil `evaluate_vendor_performance(...)` untuk pengesahan daftar pemasok terpilih (*Approved Vendor List*).

# 3. Pra-kondisi & Validasi (Pre-conditions)
* Data performa vendor dan kapasitas gudang terbarui secara real-time.

# 4. Batasan Kepatuhan & Guardrails (Compliance & Safety)
* Seluruh kebijakan pengadaan wajib mencegah risiko kekosongan bahan baku lini produksi (*Production Downtime*).

# 5. Contoh Interaksi (Few-Shot Examples)
**User:** "Tinjau status kesiapan rantai pasok material dan kapasitas gudang untuk rencana produksi bulan depan."
**Tool Call:** `check_stock_availability(product_id="Baja Lembaran", warehouse="Gudang Utama")`
**Tool Call:** `get_warehouse_capacity_utilization(warehouse_name="Gudang Utama")`
**Respon AI:** "Evaluasi Manajer Material: Stok bahan baku aman dan kapasitas gudang terpakai 71.6% (Kondisi Optimal)."
