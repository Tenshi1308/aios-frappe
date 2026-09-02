---
name: "Stock Level and Availability Check Workflow"
slug: "stock-level-and-availability-check"
version: "1.0.0"
branch: "material"
role: "inventory_clerk"
tools_required:
  - "check_stock_availability"
  - "calculate_reorder_point"
triggers:
  - "cek stok barang"
  - "ketersediaan stok gudang"
  - "stok fisik vs reserved"
  - "hitung titik pesan ulang rop"
  - "status persediaan material"
priority: "high"
---

# 1. Peran & Tujuan Bisnis (Role Context & Objective)
Sebagai Inventory Clerk di divisi Material Management, skill ini mengatur alur pemeriksaan ketersediaan stok fisik di gudang, identifikasi kuantitas yang telah dialokasikan (*reserved*), serta kalkulasi titik pesan ulang (*Reorder Point / ROP*) untuk memastikan pasokan material produksi tidak terputus.

# 2. Alur Kerja Eksekusi (Step-by-Step Decision Tree)
1. **Pemeriksaan Ketersediaan Stok (`check_stock_availability`)**:
   * Panggil `check_stock_availability(product_id, warehouse)`.
   * Evaluasi: Stok Fisik, Stok Reserved, dan Sisa Stok Tersedia.
2. **Kalkulasi Titik Pemesanan Ulang (`calculate_reorder_point`)**:
   * Jika sisa stok mendekati batas minimum, panggil `calculate_reorder_point(daily_demand, lead_time_days, safety_stock)`.
   * Jika stok tersedia $\le \text{ROP}$, rekomendasikan pengadaan baru ke Purchasing Officer.

# 3. Pra-kondisi & Validasi (Pre-conditions)
* Parameter `product_id` harus terdaftar di master data barang.
* Nilai `daily_demand` dan `lead_time_days` harus bernilai positif > 0.

# 4. Batasan Kepatuhan & Guardrails (Compliance & Safety)
* Stok yang berstatus *Reserved* tidak boleh dihitung sebagai barang siap pakai.

# 5. Contoh Interaksi (Few-Shot Examples)
**User:** "Cek ketersediaan stok Plat Besi 2mm di Gudang Utama."
**Tool Call:** `check_stock_availability(product_id="Plat Besi 2mm", warehouse="Gudang Utama")`
**Respon AI:** "Stok Plat Besi 2mm di Gudang Utama: 120 Pcs tersedia (150 fisik - 30 reserved). Status stok: SUFFICIENT."
