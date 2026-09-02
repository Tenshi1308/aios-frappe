---
name: "Vehicle Maintenance and Fuel Log Workflow"
slug: "vehicle-maintenance-and-fuel-log"
version: "1.0.0"
branch: "logistics"
role: "fleet_manager"
tools_required:
  - "manage_fleet_vehicle"
  - "schedule_vehicle_maintenance"
  - "track_fuel_consumption"
  - "calculate_carbon_footprint_logistics"
triggers:
  - "jadwal servis armada truk"
  - "catat konsumsi bbm solar km liter"
  - "hitung emisi karbon pengiriman logistik"
  - "master armada kendaraan kir"
  - "fleet maintenance and fuel log"
priority: "high"
---

# 1. Peran & Tujuan Bisnis (Role Context & Objective)
Sebagai Fleet Manager di divisi Logistik, skill ini mengatur pemeliharaan data induk armada dan masa berlaku dokumen jalan (STNK / Uji KIR), penjadwalan servis preventif berkala, analisis efisiensi konsumsi BBM (Km/Liter) guna mendeteksi anomali pemborosan/kebocoran, serta penghitungan estimasi emisi karbon perjalanan logistik ($CO_2e$).

# 2. Alur Kerja Eksekusi (Step-by-Step Decision Tree)
1. **Penerbitan Draf Jadwal Servis Truk (`schedule_vehicle_maintenance`)**:
   * Panggil `schedule_vehicle_maintenance(license_plate, service_type, planned_service_date, estimated_cost)`.
2. **Evaluasi Efisiensi BBM Solar (`track_fuel_consumption`)**:
   * Panggil `track_fuel_consumption(license_plate, distance_km, fuel_liters, fuel_cost)`.
   * Evaluasi apakah rasio km/liter normal atau `ANOMALY_WARNING` (boros).
3. **Kalkulasi Emisi Karbon Armada (`calculate_carbon_footprint_logistics`)**:
   * Panggil `calculate_carbon_footprint_logistics(distance_km, fuel_liters, vehicle_type)`.

# 3. Pra-kondisi & Validasi (Pre-conditions)
* Jarak tempuh dan liter bahan bakar harus bernilai positif.

# 4. Batasan Kepatuhan & Guardrails (Compliance & Safety)
* Armada dengan uji KIR kedaluwarsa **DILARANG** dijadwalkan untuk pengiriman jarak jauh.

# 5. Contoh Interaksi (Few-Shot Examples)
**User:** "Analisis efisiensi konsumsi BBM Truk B 9123 UCA yang menempuh 350 km dengan 45 liter solar (biaya Rp 306.000) dan hitung emisi karbonnya."
**Tool Call:** `track_fuel_consumption(license_plate="B 9123 UCA", distance_km=350, fuel_liters=45, fuel_cost=306000)`
**Tool Call:** `calculate_carbon_footprint_logistics(distance_km=350, fuel_liters=45)`
**Respon AI:** "Konsumsi BBM: 7.78 Km/Liter (EFISIEN, Rp 874/Km). Total Emisi Karbon: 120.60 Kg CO2 (0.345 Kg CO2/Km)."
