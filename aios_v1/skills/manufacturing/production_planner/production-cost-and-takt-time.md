---
name: "Production Cost and Takt Time Workflow"
slug: "production-cost-and-takt-time"
version: "1.0.0"
branch: "manufacturing"
role: "production_planner"
tools_required:
  - "calculate_production_cost"
  - "calculate_takt_time"
  - "track_work_order_progress"
  - "generate_production_variance_report"
triggers:
  - "hitung hpp produksi cogm"
  - "kalkulasi takt time pabrik"
  - "biaya manufaktur per unit"
  - "analisis varians biaya produksi"
  - "kecepatan lini produksi takt time"
priority: "high"
---

# 1. Peran & Tujuan Bisnis (Role Context & Objective)
Sebagai Production Planner, skill ini mengatur penghitungan Harga Pokok Produksi (*Cost of Goods Manufactured / COGM*), penentuan kecepatan ritme produksi sesuai permintaan pasar (*Takt Time Calculation*), serta audit perbandingan antara biaya standar dengan biaya aktual (*Production Cost Variance*).

# 2. Alur Kerja Eksekusi (Step-by-Step Decision Tree)
1. **Kalkulasi Biaya Pokok Manufaktur (`calculate_production_cost`)**:
   * Panggil `calculate_production_cost(raw_materials_cost, direct_labor_hours, hourly_labor_rate, overhead_cost, batch_quantity)`.
   * Dapatkan unit production cost per item.
2. **Penentuan Ritme Takt Time (`calculate_takt_time`)**:
   * Panggil `calculate_takt_time(available_working_time_seconds, customer_demand_units)`.
3. **Audit Varians Biaya Produksi (`generate_production_variance_report`)**:
   * Panggil `generate_production_variance_report(production_order_id, standard_cost, actual_cost)`.

# 3. Pra-kondisi & Validasi (Pre-conditions)
* Waktu kerja bersih dan kuantitas batch harus bernilai angka positif > 0.

# 4. Batasan Kepatuhan & Guardrails (Compliance & Safety)
* Varians biaya overbudget > 10% wajib dilaporkan dan mendapatkan analisis mitigasi.

# 5. Contoh Interaksi (Few-Shot Examples)
**User:** "Hitung HPP produksi 200 unit produk dengan biaya bahan Rp 40.000.000, 120 jam kerja operator @Rp 35.000, dan overhead pabrik Rp 8.000.000."
**Tool Call:** `calculate_production_cost(raw_materials_cost=40000000, direct_labor_hours=120, hourly_labor_rate=35000, overhead_cost=8000000, batch_quantity=200)`
**Respon AI:** "Total HPP Produksi adalah Rp 52.200.000 dengan Biaya Pokok per Unit sebesar Rp 261.000."
