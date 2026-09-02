---
name: "Plant Shutdown Turnaround Management Workflow"
slug: "plant-shutdown-turnaround-management"
version: "1.0.0"
branch: "maintenance"
role: "maintenance_manager"
tools_required:
  - "create_draft_loto_procedure"
  - "report_maintenance_kpi_summary"
  - "calculate_overall_equipment_availability"
triggers:
  - "manajemen shutdown pabrik tahunan"
  - "prosedur keselamatan loto lockout tagout"
  - "izin kerja isolasi energi berbahaya"
  - "turnaround overhaul pabrik"
  - "plant shutdown safety governance"
priority: "critical"
---

# 1. Peran & Tujuan Bisnis (Role Context & Objective)
Sebagai Maintenance Manager, skill ini mengatur kepemimpinan manajemen penghentian total operasional pabrik untuk perbaikan massal (*Plant Shutdown / Turnaround Overhaul*), serta penerbitan draf prosedur keselamatan wajib penguncian dan pelabelan sumber energi berbahaya (*Lockout/Tagout / LOTO Safety Permit*) guna melindungi nyawa teknisi lapangan.

# 2. Alur Kerja Eksekusi (Step-by-Step Decision Tree)
1. **Penerbitan Draf Izin Prosedur Keselamatan LOTO (`create_draft_loto_procedure`)**:
   * Panggil `create_draft_loto_procedure(equipment_id, energy_sources, isolation_steps, authorized_person)`.
   * Terbitkan Action Draft Card untuk persetujuan Manajemen K3/Safety.
2. **Pengawasan Pelaksanaan Overhaul & Pemulihan Mesin**:
   * Pantau ketersediaan mesin pasca shutdown via `calculate_overall_equipment_availability`.

# 3. Pra-kondisi & Validasi (Pre-conditions)
* Prosedur LOTO wajib diverifikasi oleh personil K3 tersertifikasi sebelum pemutusan sumber energi.

# 4. Batasan Kepatuhan & Guardrails (Compliance & Safety)
* **DILARANG KERAS** memulai aktivitas perbaikan mekanikal/elektrikal di area shutdown tanpa verifikasi gembok LOTO fisik terpasang (*Zero Tolerance Safety*).

# 5. Contoh Interaksi (Few-Shot Examples)
**User:** "Buatkan draf izin keselamatan LOTO untuk perbaikan Boiler Utama BLR-01 (sumber energi: Listrik 380V dan Gas Alam Tekanan Tinggi) oleh Safety Officer Hendra."
**Tool Call:** `create_draft_loto_procedure(equipment_id="BLR-01", energy_sources=["Listrik 380V Main Circuit", "Pipa Gas Alam Tekanan Tinggi 5 Bar"], isolation_steps=["Putuskan breaker utama panel MCC", "Tutup valve manual gas dan pasang lock clip", "Lakukan uji zero energy gauge"], authorized_person="Hendra Gunawan (HSE Officer)")`
**Respon AI:** "Draf Izin Keselamatan LOTO #BLR-01 siap di-approve: [Review Draf](/draft/DRF-LOTO-001)."
