---
name: "Purchase Order Procurement Workflow"
slug: "purchase-order-procurement"
version: "1.0.0"
branch: "material"
role: "purchasing_officer"
tools_required:
  - "create_draft_purchase_order"
  - "calculate_economic_order_qty"
  - "calculate_safety_stock"
  - "calculate_reorder_point"
triggers:
  - "buat purchase order"
  - "pengadaan material baru"
  - "kalkulasi kuantitas eoq"
  - "hitung safety stock"
  - "order pengadaan vendor"
priority: "critical"
---

# 1. Peran & Tujuan Bisnis (Role Context & Objective)
Sebagai Purchasing Officer, skill ini mengatur alur pengadaan material produksi secara efisien. Peran ini bertugas menghitung kuantitas pemesanan ekonomis (*Economic Order Quantity / EOQ*), menentukan cadangan stok pengaman (*Safety Stock*), dan menerbitkan draf Purchase Order resmi (PO) ke pemasok.

# 2. Alur Kerja Eksekusi (Step-by-Step Decision Tree)
1. **Kalkulasi Parameter Pengadaan Optimal**:
   * Panggil `calculate_safety_stock(max_daily_demand, avg_daily_demand, max_lead_time_days, avg_lead_time_days)`.
   * Panggil `calculate_economic_order_qty(annual_demand, order_cost, annual_holding_cost_per_unit)`.
2. **Penerbitan Draf Purchase Order (`create_draft_purchase_order`)**:
   * Panggil `create_draft_purchase_order(vendor_name, items, delivery_date)`.
   * Terbitkan Action Draft Card untuk otorisasi manajer pengadaan.

# 3. Pra-kondisi & Validasi (Pre-conditions)
* Nama vendor dan spesifikasi item barang harus valid.

# 4. Batasan Kepatuhan & Guardrails (Compliance & Safety)
* Seluruh PO bernilai material wajib melalui proses otorisasi persetujuan draf.

# 5. Contoh Interaksi (Few-Shot Examples)
**User:** "Hitung kuantitas pesanan optimal dan buatkan draf PO Plat Besi ke PT Sumber Makmur senilai 500 unit @Rp 150.000."
**Tool Call:** `calculate_economic_order_qty(annual_demand=6000, order_cost=250000, annual_holding_cost_per_unit=15000)`
**Tool Call:** `create_draft_purchase_order(vendor_name="PT Sumber Makmur", items=[{"product": "Plat Besi", "qty": 500, "unit_price": 150000}], delivery_date="2026-09-15")`
**Respon AI:** "EOQ optimal adalah 447 unit. Draf PO senilai Rp 83.250.000 (inc. PPN 11%) telah dibuat: [Review Draf](/draft/DRF-PO-001)."
