---
name: "Route Planning and Tracking Workflow"
slug: "route-planning-and-tracking"
version: "1.0.0"
branch: "logistics"
role: "logistics_coordinator"
tools_required:
  - "plan_shipment_route"
  - "track_shipment_status"
  - "log_pod_proof_of_delivery"
triggers:
  - "buat rencana rute pengiriman"
  - "multi stop delivery route"
  - "estimasi jarak dan waktu tempuh armada"
  - "lacak posisi truk logistik"
  - "route planning optimization"
priority: "high"
---

# 1. Peran & Tujuan Bisnis (Role Context & Objective)
Sebagai Logistics Coordinator, skill ini mengatur perancangan rute pengiriman multi-titik (*Multi-Stop Route Planning*), estimasi jarak tempuh dan waktu tiba (*ETA*), serta pemantauan pergerakan armada secara langsung (*Real-time Shipment Tracking*).

# 2. Alur Kerja Eksekusi (Step-by-Step Decision Tree)
1. **Perancangan Draf Rencana Rute Multi-Drop (`plan_shipment_route`)**:
   * Panggil `plan_shipment_route(origin_warehouse, destination_stops, vehicle_type)`.
   * Dapatkan total estimasi jarak (`est_distance_km`) dan durasi tempuh (`est_time_hours`).
2. **Pemantauan Status Posisi Armada (`track_shipment_status`)**:
   * Panggil `track_shipment_status(tracking_number)`.

# 3. Pra-kondisi & Validasi (Pre-conditions)
* Urutan alamat destinasi harus diatur secara geografis paling efisien.

# 4. Batasan Kepatuhan & Guardrails (Compliance & Safety)
* Waktu tempuh perjalanan pengemudi wajib memperhitungkan batas jam istirahat keselamatan (*Driver Fatigue Rules*).

# 5. Contoh Interaksi (Few-Shot Examples)
**User:** "Rencanakan rute pengiriman dari Gudang Cikarang ke 3 toko di Bekasi, Jakarta Timur, dan Jakarta Utara menggunakan armada Truk CDD 4 Ton."
**Tool Call:** `plan_shipment_route(origin_warehouse="Gudang Utama Cikarang", destination_stops=[{"addr": "Toko A Bekasi"}, {"addr": "Toko B Jaktim"}, {"addr": "Toko C Jakut"}], vehicle_type="Truk CDD 4 Ton")`
**Respon AI:** "Draf Rencana Rute (3 titik, 75 km, est. 2.1 jam) berhasil dibuat: [Review Draf](/draft/DRF-ROU-001)."
