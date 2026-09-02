---
name: "Customs and Cross Border Compliance Workflow"
slug: "customs-and-cross-border-compliance"
version: "1.0.0"
branch: "logistics"
role: "logistics_manager"
tools_required:
  - "calculate_freight_demurrage"
  - "report_transit_damage"
  - "create_draft_cross_docking"
triggers:
  - "hitung demurrage pelabuhan denda kontainer"
  - "klaim asuransi kerusakan transit"
  - "kepatuhan logistik ekspor impor"
  - "waktu tunggu kontainer dwell time"
  - "cross border freight compliance"
priority: "high"
---

# 1. Peran & Tujuan Bisnis (Role Context & Objective)
Sebagai Logistics Manager di divisi Logistik, skill ini mengatur pengawasan biaya demurrage/detention di pelabuhan peti kemas (*Port Freight Demurrage Management*), penerbitan draf klaim asuransi atas insiden kerusakan barang selama perjalanan transit (*Transit Damage Claim*), serta koordinasi fasilitas transit cepat (*Cross-Docking*).

# 2. Alur Kerja Eksekusi (Step-by-Step Decision Tree)
1. **Penghitungan Biaya Denda Demurrage Kontainer (`calculate_freight_demurrage`)**:
   * Panggil `calculate_freight_demurrage(free_days_allowed, actual_dwell_days, daily_demurrage_rate, container_count)`.
2. **Penerbitan Draf Klaim Kerusakan Transit (`report_transit_damage`)**:
   * Jika terjadi kecelakaan/kerusakan barang di perjalanan, panggil `report_transit_damage(shipment_id, damaged_items, estimated_loss_amount, incident_description)`.

# 3. Pra-kondisi & Validasi (Pre-conditions)
* Data durasi penumpukan peti kemas harus divalidasi dengan manifes pelabuhan.

# 4. Batasan Kepatuhan & Guardrails (Compliance & Safety)
* Klaim kerusakan transit wajib dilampiri bukti berita acara kepolisian atau laporan surveyor asuransi resmi.

# 5. Contoh Interaksi (Few-Shot Examples)
**User:** "Hitung biaya denda demurrage untuk 3 kontainer yang tertahan 10 hari di Pelabuhan Tanjung Priok (batas gratis 5 hari, tarif Rp 750.000/hari/kontainer)."
**Tool Call:** `calculate_freight_demurrage(free_days_allowed=5, actual_dwell_days=10, daily_demurrage_rate=750000, container_count=3)`
**Respon AI:** "Total denda Demurrage (5 hari penalti, 3 kontainer) adalah Rp 11.250.000."
