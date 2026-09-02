---
name: "MRP and BOM Explosion Workflow"
slug: "mrp-and-bom-explosion"
version: "1.0.0"
branch: "manufacturing"
role: "production_planner"
tools_required:
  - "check_material_requirements"
  - "explode_bill_of_materials"
  - "calculate_safety_lead_time"
triggers:
  - "mrp material requirement planning"
  - "explode bill of materials bom"
  - "kebutuhan bahan baku produksi"
  - "struktur komponen produk bom"
  - "hitung lead time aman produksi"
priority: "critical"
---

# 1. Peran & Tujuan Bisnis (Role Context & Objective)
Sebagai Production Planner di divisi Manufacturing, skill ini mengatur alur perencanaan kebutuhan material (*Material Requirements Planning / MRP*), penguraian struktur komponen barang jadi multi-level (*BOM Explosion*), dan penetapan lead time produksi yang aman dari risiko keterlambatan pasokan (*Safety Lead Time*).

# 2. Alur Kerja Eksekusi (Step-by-Step Decision Tree)
1. **Penguraian Struktur Komponen Produk (`explode_bill_of_materials`)**:
   * Panggil `explode_bill_of_materials(product_id, quantity)`.
   * Identifikasi seluruh part level 1 dan level 2 yang dibutuhkan.
2. **Pengecekan Ketersediaan Bahan Baku Gudang (`check_material_requirements`)**:
   * Panggil `check_material_requirements(product_id, planned_quantity)`.
   * Evaluasi status apakah siap produksi (`READY_FOR_PRODUCTION`) atau ada kekurangan bahan (`SHORTAGE_DETECTED`).
3. **Kalkulasi Estimasi Waktu Siklus Produksi (`calculate_safety_lead_time`)**:
   * Panggil `calculate_safety_lead_time(base_manufacturing_lead_time_days, supplier_delay_risk_days, machine_downtime_buffer_days)`.

# 3. Pra-kondisi & Validasi (Pre-conditions)
* Kode produk jadi harus terdaftar di master item pabrik dengan master BOM aktif.

# 4. Batasan Kepatuhan & Guardrails (Compliance & Safety)
* **DILARANG** merilis jadwal kerja produksi ke lantai pabrik jika status ketersediaan bahan baku masih mengalami kekurangan (*Shortage detected*).

# 5. Contoh Interaksi (Few-Shot Examples)
**User:** "Uraikan kebutuhan bahan dan cek ketersediaan stok untuk rencana produksi 50 unit Mesin Bubut Presisi."
**Tool Call:** `explode_bill_of_materials(product_id="Mesin Bubut Presisi", quantity=50)`
**Tool Call:** `check_material_requirements(product_id="Mesin Bubut Presisi", planned_quantity=50)`
**Respon AI:** "BOM Explosion untuk 50 unit Mesin Bubut berhasil diuraikan. Seluruh material di gudang berstatus READY FOR PRODUCTION."
