---
name: "Freight Cost and Load Optimization Workflow"
slug: "freight-cost-and-load-optimization"
version: "1.0.0"
branch: "logistics"
role: "logistics_coordinator"
tools_required:
  - "calculate_shipping_cost"
  - "optimize_load_planning"
triggers:
  - "hitung ongkir ongkos kirim logistik"
  - "berat volumetrik p x l x t"
  - "optimasi muatan truk cbm kubikasi"
  - "kapasitas tonase truk kargo"
  - "freight cost load optimization"
priority: "high"
---

# 1. Peran & Tujuan Bisnis (Role Context & Objective)
Sebagai Logistics Coordinator, skill ini mengatur penghitungan akurat ongkos kirim (*Freight Costing*) berdasarkan perbandingan berat aktual vs berat volumetrik ($P \times L \times T / 5000$), jarak, serta optimasi pemanfaatan ruang muatan truk/kontainer (*Load Planning Optimization*) agar armada tidak *overload* atau membawa ruang kosong berlebih.

# 2. Alur Kerja Eksekusi (Step-by-Step Decision Tree)
1. **Penghitungan Ongkos Kirim & Berat Ditagih (`calculate_shipping_cost`)**:
   * Panggil `calculate_shipping_cost(weight_kg, length_cm, width_cm, height_cm, distance_km, service_tier)`.
   * Evaluasi berat yang ditagih (`chargeable_weight_kg`).
2. **Optimasi Utilisasi Ruang Muatan Armada (`optimize_load_planning`)**:
   * Panggil `optimize_load_planning(truck_max_weight_kg, truck_max_cbm, cargo_items)`.
   * Periksa apakah status `OPTIMAL_LOAD` atau `OVERLOAD_ALERT`.

# 3. Pra-kondisi & Validasi (Pre-conditions)
* Dimensi kemasan (P, L, T) dan berat harus berupa angka positif.

# 4. Batasan Kepatuhan & Guardrails (Compliance & Safety)
* **DILARANG KERAS** memberangkatkan truk jika utilisasi berat $> 100\%$ (*Overdimension Overload / ODOL Restriction*).

# 5. Contoh Interaksi (Few-Shot Examples)
**User:** "Hitung ongkos kirim paket berukuran 60x50x40 cm dengan berat 15 kg untuk jarak 120 km layanan Regular."
**Tool Call:** `calculate_shipping_cost(weight_kg=15, length_cm=60, width_cm=50, height_cm=40, distance_km=120, service_tier="Regular")`
**Respon AI:** "Berat aktual 15 kg vs berat volumetrik 24.0 kg. Berat yang ditagih: 24.0 kg. Total Ongkos Kirim: Rp 259.200."
