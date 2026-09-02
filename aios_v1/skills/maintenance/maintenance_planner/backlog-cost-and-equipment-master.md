---
name: "Backlog Cost and Equipment Master Workflow"
slug: "backlog-cost-and-equipment-master"
version: "1.0.0"
branch: "maintenance"
role: "maintenance_planner"
tools_required:
  - "generate_maintenance_backlog"
  - "estimate_maintenance_cost"
  - "manage_equipment_master"
  - "verify_warranty_status"
triggers:
  - "pantau antrean backlog servis mesin"
  - "hitung estimasi biaya perawatan"
  - "master data mesin pabrik aset"
  - "cek garansi mesin oem"
  - "maintenance cost estimation"
priority: "high"
---

# 1. Peran & Tujuan Bisnis (Role Context & Objective)
Sebagai Maintenance Planner, skill ini mengatur pemantauan antrean pekerjaan servis mesin yang tertunda (*Overdue Maintenance Backlog*), penghitungan estimasi biaya total pemeliharaan (Suku Cadang + Biaya Jam Kerja Teknisi + Jasa Vendor Luar), pengelolaan data master mesin aset pabrik, serta verifikasi status masa garansi dari pihak manufaktur OEM.

# 2. Alur Kerja Eksekusi (Step-by-Step Decision Tree)
1. **Pemantauan Antrean Servis Tertunda (`generate_maintenance_backlog`)**:
   * Panggil `generate_maintenance_backlog(department)`.
2. **Estimasi Biaya Perawatan Mesin (`estimate_maintenance_cost`)**:
   * Panggil `estimate_maintenance_cost(spare_parts_cost, technician_hours, hourly_rate, third_party_service_cost)`.
3. **Pemeriksaan Garansi & Master Mesin**:
   * Panggil `verify_warranty_status(equipment_id)` dan `manage_equipment_master(...)`.

# 3. Pra-kondisi & Validasi (Pre-conditions)
* Parameter estimasi biaya harus bernilai numerik non-negatif.

# 4. Batasan Kepatuhan & Guardrails (Compliance & Safety)
* Jika mesin masih dalam masa garansi OEM aktif, perbaikan komponen utama disarankan menggunakan vendor resmi agar garansi tidak gugur.

# 5. Contoh Interaksi (Few-Shot Examples)
**User:** "Hitung estimasi biaya servis overhaul jika biaya suku cadang Rp 8.000.000, jam kerja teknisi 16 jam (@ Rp 75.000/jam), dan jasa kalibrasi luar Rp 2.500.000."
**Tool Call:** `estimate_maintenance_cost(spare_parts_cost=8000000, technician_hours=16, hourly_rate=75000, third_party_service_cost=2500000)`
**Respon AI:** "Estimasi Biaya Servis Overhaul: Total Rp 11.700.000 (Suku Cadang: Rp 8.000.000, Tenaga Kerja: Rp 1.200.000, Jasa Luar: Rp 2.500.000)."
