---
name: "Driver Assignment and Dispatch Workflow"
slug: "driver-assignment-and-dispatch"
version: "1.0.0"
branch: "logistics"
role: "fleet_manager"
tools_required:
  - "manage_fleet_vehicle"
  - "track_fuel_consumption"
  - "calculate_carbon_footprint_logistics"
triggers:
  - "penugasan supir pengemudi armada"
  - "alokasi armada truk trip pengiriman"
  - "dispatch sopir logistik"
  - "jadwal keberangkatan supir"
  - "driver vehicle dispatching"
priority: "high"
---

# 1. Peran & Tujuan Bisnis (Role Context & Objective)
Sebagai Fleet Manager, skill ini mengatur penugasan pengemudi berlisensi aktif (*Driver Assignment*) ke armada truk yang layak jalan, pengawasan kesiapan kelengkapan dokumen perjalanan, serta evaluasi operasional armada sebelum keberangkatan (*Pre-Trip Dispatch Check*).

# 2. Alur Kerja Eksekusi (Step-by-Step Decision Tree)
1. **Pemeriksaan Kelayakan Armada (`manage_fleet_vehicle`)**:
   * Periksa masa berlaku STNK dan uji KIR kendaraan.
2. **Pengawasan Konsumsi Bahan Bakar & Jejak Karbon Pengemudi**:
   * Panggil `track_fuel_consumption` dan `calculate_carbon_footprint_logistics` untuk evaluasi perilaku berkendara hemat energi (*Eco-Driving*).

# 3. Pra-kondisi & Validasi (Pre-conditions)
* Pengemudi harus memiliki SIM (B1/B2 Umum) yang masih berlaku.

# 4. Batasan Kepatuhan & Guardrails (Compliance & Safety)
* Pengemudi yang telah bertugas $\ge 8$ jam wajib dialokasikan waktu istirahat minimal 1 jam sebelum trip berikutnya.

# 5. Contoh Interaksi (Few-Shot Examples)
**User:** "Periksa kesiapan armada Truk Wingbox B 9901 UXZ (max 12 ton) untuk penugasan pengiriman Jakarta - Surabaya."
**Tool Call:** `manage_fleet_vehicle(license_plate="B 9901 UXZ", vehicle_model="Hino Ranger 500", vehicle_type="Wingbox", max_payload_kg=12000, stnk_expiry="2027-08-10", kir_expiry="2027-02-15")`
**Respon AI:** "Draf Master Armada B 9901 UXZ berhasil diverifikasi dan siap ditugaskan: [Review Draf](/draft/DRF-FLT-001)."
